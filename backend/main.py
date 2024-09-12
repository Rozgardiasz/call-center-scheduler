from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from models import WorkHour, Vacation
import schemas
import crud
from auth import get_current_active_admin, get_current_user, create_jwt_token

from database import SessionLocal, Base, engine

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# List of allowed origins
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080"  # Add any other origins if needed
]

# Adding CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows these origins
    allow_credentials=True,  # Allows sending cookies with cross-origin requests
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers (e.g., Authorization)
)



Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/login")
async def login(credentials: schemas.EmployeeLogin, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, credentials)
    if user:
        token = create_jwt_token({"user_id": user.id})
        return {"token": token, "is_admin" : user.is_admin, "first_name" : user.first_name, "last_name" : user.last_name}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/admin/add_user")
def add_user(user: schemas.EmployeeCreate, request: Request, db: Session = Depends(get_db)):
    get_current_active_admin(request, db)  # Ensure user is admin

    # Add the employee
    employee = crud.add_employee(db, user)

    # Add work hours for the employee
    for work_hour in user.work_hours:
        crud.add_work_hour(db, employee.id, work_hour)

    return {"message": "User and work hours added successfully"}


@app.post("/holiday_request")
def request_holiday(holiday: schemas.VacationCreate, request: Request, db: Session = Depends(get_db)):
    get_current_user(request, db)  # Ensure user is authenticated
    new_holiday = Vacation(
        employee_id=holiday.employee_id,
        vacation_start=holiday.vacation_start,
        vacation_end=holiday.vacation_end,
        type_of_vacation=holiday.type_of_vacation,
        status='pending'
    )
    
    if not crud.can_request_more_holidays(db, holiday.employee_id, new_holiday):
        if new_holiday.type_of_vacation == "on_demand":
            raise HTTPException(status_code=400, detail="On-demand leave limit reached")
        else:
            raise HTTPException(status_code=400, detail="Leave limit reached")
    
    crud.create_vacation_request(db, new_holiday)
    return {"message": "Holiday request submitted successfully"}


@app.post("/admin/approve_holiday/{holiday_id}", status_code = 200)
def approve_holiday(holiday_id: int, request: Request, db: Session = Depends(get_db)):
    get_current_active_admin(request, db)  # Ensure user is admin
    vacation = crud.get_vacation_request(db, holiday_id)
    if vacation.type_of_vacation == "on_demand":
        crud.approve_vacation_request(db, holiday_id)

    if not crud.is_holiday_approval_possible(db, vacation.employee_id, vacation.vacation_start, vacation.vacation_end):
        raise HTTPException(status_code=400, detail="Not enough workers available")
    crud.approve_vacation_request(db, holiday_id)

@app.post("/admin/reject_holiday/{holiday_id}",status_code = 200)
def reject_holiday(holiday_id: int, request: Request, db: Session = Depends(get_db)):
    get_current_active_admin(request, db)  # Ensure user is admin
    vacation = crud.get_vacation_request(db, holiday_id)
    if vacation.status != 'pending':
        raise HTTPException(status_code=400, detail="Vacation request is not pending")
    crud.reject_vacation_request(db, holiday_id)


@app.get("/is_admin")
def check_if_admin(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    if current_user.is_admin:
        return {"is_admin": True}
    return {"is_admin": False}


@app.get("/working_hours")
def view_working_hours(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    working_hours = db.query(WorkHour).filter(WorkHour.employee_id == current_user.id).all()
    return {"work_hours": working_hours}


@app.get("/holidays/pending")
def get_pending_holidays(request: Request, db: Session = Depends(get_db)):
    get_current_active_admin(request, db)  # Ensure user is admin
    pending_holidays = crud.get_pending_holidays(db)
    
    # Formatowanie zwróconych danych, uwzględniając pracownika
    return [
        {
            "id": holiday.Vacation.id,
            "employee_id": holiday.Employee.id,
            "first_name": holiday.Employee.first_name,  # Zaciągnięte z powiązanego pracownika
            "last_name": holiday.Employee.last_name,    # Zaciągnięte z powiązanego pracownika
            "vacation_start": holiday.Vacation.vacation_start,
            "vacation_end": holiday.Vacation.vacation_end,
            "type_of_vacation": holiday.Vacation.type_of_vacation,
            "status": holiday.Vacation.status
        }
        for holiday in pending_holidays
    ]



@app.get("/holidays/{user_id}", response_model=List[schemas.Vacation])
def get_user_holidays(user_id: int, request: Request, db: Session = Depends(get_db)):
    # get_current_active_admin(request, db)  # Ensure user is admin
    user_holidays = crud.get_user_holidays(db, user_id)
    return user_holidays

@app.get("/admin/users", response_model=List[schemas.Employee])
def get_all_users(request: Request, db: Session = Depends(get_db)):
    get_current_active_admin(request, db)  # Ensure user is admin
    all_users = crud.get_all_users(db)
    return all_users

@app.delete("/admin/remove_user/{user_id}")
def remove_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    # Ensure the user making the request is an admin
    current_admin = get_current_active_admin(request, db)
    if not current_admin:
        raise HTTPException(status_code=403, detail="Only admins can remove users")

    # Fetch the user from the database
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_admin:
        raise HTTPException(status_code=403, detail="Admins cannot be removed")

    # Delete the user from the database
    crud.delete_user(db, user_id)
    return {"message": "User successfully removed"}


@app.post("/can_approve_holiday")
def can_approve_holiday(request: Request, holiday: schemas.VacationCreate, db: Session = Depends(get_db)):
    user = get_current_user(request, db)

    # Convert string to datetime
    try:
        vacation_start = datetime.strptime(holiday.vacation_start, "%Y-%m-%d")
        vacation_end = datetime.strptime(holiday.vacation_end, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    if not crud.can_request_more_holidays(db, user.id):
        return {"can_approve": False, "message": "Holiday limit reached."}

    if not crud.is_holiday_approval_possible(db, user.id, vacation_start, vacation_end):
        return {"can_approve": False, "message": "Not enough workers available during your vacation."}

    return {"can_approve": True, "message": "Your holiday request can be approved."}