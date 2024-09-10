from sqlalchemy.orm import Session
from models import Employee, Vacation, WorkHour
from hashlib import sha256
import schemas
from datetime import datetime


def authenticate_user(db: Session, credentials: schemas.EmployeeLogin):
    user = db.query(Employee).filter(Employee.email == credentials.email).first()
    if user and sha256(credentials.password.encode()).hexdigest() == user.password:
        return user
    return None

def get_pending_holidays(db: Session):
    return db.query(Vacation).filter(Vacation.status == 'pending').all()

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


def is_holiday_approval_possible(db: Session, employee_id: int, vacation_start: datetime,
                                 vacation_end: datetime) -> bool:
    MIN_WORKERS_REQUIRED = 3
    overlapping_work_hours = db.query(WorkHour).filter(
        WorkHour.employee_id != employee_id,
        WorkHour.weekday.in_([vacation_start.strftime('%A'), vacation_end.strftime('%A')])
    ).all()
    available_workers = len(overlapping_work_hours)
    return available_workers >= MIN_WORKERS_REQUIRED


def can_request_more_holidays(db: Session, employee_id: int) -> bool:
    HOLIDAY_LIMIT = 20
    approved_holidays_count = db.query(Vacation).filter(
        Vacation.employee_id == employee_id,
        Vacation.status == 'approved'
    ).count()
    return approved_holidays_count < HOLIDAY_LIMIT
