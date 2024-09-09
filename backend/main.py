from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from models import WorkHour
import schemas
import crud
from auth import get_current_active_admin, get_current_user, create_jwt_token

from database import SessionLocal, Base, engine

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# List of allowed origins
origins = [
    "http://localhost:8080"
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
    if not crud.can_request_more_holidays(db, holiday.employee_id):
        raise HTTPException(status_code=400, detail="Holiday limit reached")
    crud.create_vacation_request(db, holiday)


@app.post("/admin/approve_holiday")
def approve_holiday(holiday_id: int, request: Request, db: Session = Depends(get_db)):
    get_current_active_admin(request, db)  # Ensure user is admin
    vacation = crud.get_vacation_request(db, holiday_id)
    if not crud.is_holiday_approval_possible(db, vacation.employee_id, vacation.vacation_start, vacation.vacation_end):
        raise HTTPException(status_code=400, detail="Not enough workers available")
    crud.approve_vacation_request(db, holiday_id)


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
