from sqlalchemy.orm import Session
from models import Employee, Vacation, WorkHour
from hashlib import sha256
import schemas
from datetime import datetime, timedelta
from fastapi import HTTPException


def authenticate_user(db: Session, credentials: schemas.EmployeeLogin):
    user = db.query(Employee).filter(Employee.email == credentials.email).first()
    if user and sha256(credentials.password.encode()).hexdigest() == user.password:
        return user
    return None

def get_pending_holidays(db: Session):
    return db.query(Vacation, Employee).join(Employee).filter(Vacation.status == "pending").all()

def get_user_holidays(db: Session, user_id: int):
    return db.query(Vacation).filter(Vacation.employee_id == user_id).all()

def get_all_users(db: Session):
    return db.query(Employee).all()



def add_employee(db: Session, employee_data: schemas.EmployeeCreate) -> Employee:
    # Create and add the employee to the database
    employee = Employee(
        first_name=employee_data.first_name,
        last_name=employee_data.last_name,
        email=employee_data.email,
        password=sha256(employee_data.password.encode()).hexdigest()
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def add_work_hour(db: Session, employee_id: int, work_hour_data: schemas.WorkHourCreate):
    work_hour = WorkHour(
        employee_id=employee_id,
        weekday=work_hour_data.weekday,
        start_time=work_hour_data.start_time,
        end_time=work_hour_data.end_time
    )
    db.add(work_hour)
    db.commit()


def create_vacation_request(db: Session, holiday: schemas.VacationCreate):
    db_vacation = Vacation(
        employee_id=holiday.employee_id,
        vacation_start=holiday.vacation_start,
        vacation_end=holiday.vacation_end,
        type_of_vacation=holiday.type_of_vacation
    )
    db.add(db_vacation)
    db.commit()
    db.refresh(db_vacation)
    return db_vacation


def get_vacation_request(db: Session, holiday_id: int):
    return db.query(Vacation).filter(Vacation.id == holiday_id).first()


def approve_vacation_request(db: Session, holiday_id: int):
    vacation = db.query(Vacation).filter(Vacation.id == holiday_id).first()
    if vacation:
        vacation.status = 'approved'
        db.commit()
        db.refresh(vacation)
        return vacation
    return None


from datetime import datetime, time

from datetime import datetime, time
from sqlalchemy.orm import Session
from models import WorkHour  # Adjust import based on your project structure

from datetime import datetime, time
from sqlalchemy.orm import Session

def is_holiday_approval_possible(db: Session, employee_id: int, vacation_start: datetime, vacation_end: datetime) -> bool:
    # Define minimum workers for different conditions
    MIN_WORKERS_DEFAULT = 1
    MIN_WORKERS_WEEKEND = 0
    MIN_WORKERS_HOLIDAY = 0
    MIN_WORKERS_BUSINESS_HOURS = 2
    
    # Define business hours (not used directly here but can be useful for other checks)
    business_start = time(8, 0)  # 08:00 AM
    business_end = time(16, 0)   # 04:00 PM

    # List of predefined holidays (only dates, no times)
    holidays = [
        datetime(2024, 12, 25).date(),  # Example: Christmas
        datetime(2024, 1, 1).date(),    # Example: New Year's Day
        # Add more holidays as needed
    ]

    # Convert vacation_start and vacation_end to date objects
    vacation_start_date = vacation_start
    vacation_end_date = vacation_end

    # Check if any date in the vacation period falls on a holiday
    is_holiday = any(
        vacation_start_date <= holiday <= vacation_end_date
        for holiday in holidays
    )
    
    if is_holiday:
        min_workers_required = MIN_WORKERS_HOLIDAY
    else:
        # Check if any date in the vacation period falls on a weekend
        is_weekend = any(
            (vacation_start_date + timedelta(days=i)).weekday() in (5, 6)
            for i in range((vacation_end_date - vacation_start_date).days + 1)
        )
        if is_weekend:
            min_workers_required = MIN_WORKERS_WEEKEND
        else:
            # For business hours, we assume the whole day is checked
            min_workers_required = MIN_WORKERS_BUSINESS_HOURS

    # Query overlapping work hours to check the number of available workers
    overlapping_work_hours = db.query(WorkHour).filter(
        WorkHour.employee_id != employee_id,
        WorkHour.weekday.in_([vacation_start.strftime('%A'), vacation_end.strftime('%A')])
    ).all()

    available_workers = len(overlapping_work_hours)
    print(f"{available_workers=}\n{min_workers_required=}")

    return available_workers >= min_workers_required


def can_request_more_holidays(db: Session, employee_id: int) -> bool:
    HOLIDAY_LIMIT = 20
    approved_holidays_count = db.query(Vacation).filter(
        Vacation.employee_id == employee_id,
        Vacation.status == 'approved'
    ).count()
    return approved_holidays_count < HOLIDAY_LIMIT

def reject_vacation_request(db: Session, holiday_id: int):
    vacation = db.query(Vacation).filter(Vacation.id == holiday_id).first()
    if vacation:
        vacation.status = 'rejected'
        db.commit()


def get_user_by_id(db: Session, user_id: int):
    return db.query(Employee).filter(Employee.id == user_id).first()

def delete_user(db: Session, user_id: int):

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Remove associated holiday requests
    holidays = db.query(Vacation).filter(Vacation.employee_id == user_id).all()
    for holiday in holidays:
        db.delete(holiday)

    # Remove associated work hours
    work_hours = db.query(WorkHour).filter(WorkHour.employee_id == user_id).all()
    for work_hour in work_hours:
        db.delete(work_hour)

    # Delete the user
    db.delete(user)

    # Commit the changes to the database
    db.commit()
