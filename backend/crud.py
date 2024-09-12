from sqlalchemy.orm import Session
from models import Employee, Vacation, WorkHour
from hashlib import sha256
import schemas
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy import or_, and_


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

    # Get the employee's work hours during the vacation period
    employee_work_hours = db.query(WorkHour).filter(
        WorkHour.employee_id == employee_id,
        WorkHour.weekday.in_([vacation_start.strftime('%a'), vacation_end.strftime('%a')])
    ).all()

    if not employee_work_hours:
        # No specific work hours found for the employee, assume default conditions
        print(f"{employee_work_hours=}")
        return False

    # Check for overlapping work hours with other employees during the requested vacation period
    for work_hour in employee_work_hours:
        overlapping_work_hours = db.query(WorkHour).filter(
            WorkHour.employee_id != employee_id,  # Other employees only
            WorkHour.weekday == work_hour.weekday,  # Same weekday as the employee's work hour
            or_(
                and_(WorkHour.start_time <= work_hour.start_time, WorkHour.end_time >= work_hour.start_time),  # Overlap with employee's start
                and_(WorkHour.start_time <= work_hour.end_time, WorkHour.end_time >= work_hour.end_time)  # Overlap with employee's end
            )
        ).all()

        available_workers = len(overlapping_work_hours)
        print(f"{available_workers=}\n{min_workers_required=}")

        # If not enough workers are available during any of the employee's work hours, return False
        if available_workers < min_workers_required:
            return False

    return True


from sqlalchemy.orm import Session
from datetime import date, timedelta
from models import Vacation

def can_request_more_holidays(db: Session, employee_id: int, new_holiday: Vacation) -> bool:
    # Define limits
    TOTAL_LEAVE_DAYS = 20
    TOTAL_ON_DEMAND_LEAVE_DAYS = 4
    
    year = new_holiday.vacation_start.year
    
    # Query approved holidays for the employee
    holidays = db.query(Vacation).filter(
        Vacation.employee_id == employee_id,
        Vacation.status == 'approved'
    ).all()
    
    # Fetch working hours for the employee
    employee_work_hours = db.query(WorkHour).filter(
        WorkHour.employee_id == employee_id
    ).all()

    # Create a dictionary of working days based on the WorkHour table
    working_days = {work_hour.weekday: True for work_hour in employee_work_hours}
    
    total_days_taken = 0
    total_demand_days_taken = 0

    # Include the new holiday request in the calculations
    all_holidays = holidays + [new_holiday]

    for holiday in all_holidays:
        start_date = holiday.vacation_start
        end_date = holiday.vacation_end

        if start_date.year <= year <= end_date.year:
            start_of_year = date(year, 1, 1)
            end_of_year = date(year, 12, 31)
            actual_start = max(start_date, start_of_year)
            actual_end = min(end_date, end_of_year)

            current_date = actual_start
            while current_date <= actual_end:
                day_of_week = current_date.strftime('%a')
                if working_days.get(day_of_week, False):
                    total_days_taken += 1
                    if holiday.type_of_vacation == "on_demand":
                        total_demand_days_taken += 1
                current_date += timedelta(days=1)

    remaining_leave_days = TOTAL_LEAVE_DAYS - total_days_taken
    remaining_demand_days = TOTAL_ON_DEMAND_LEAVE_DAYS - total_demand_days_taken

    if remaining_leave_days < 0:
        remaining_leave_days = 0
    if remaining_demand_days < 0:
        remaining_demand_days = 0

    if new_holiday.type_of_vacation == "on_demand":
        return remaining_demand_days > 0
    else:
        return remaining_leave_days > 0


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
