from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    is_admin: Optional[bool] = False


class WorkHourCreate(BaseModel):
    weekday: str
    start_time: str
    end_time: str


class EmployeeCreate(EmployeeBase):
    password: str
    work_hours: List[WorkHourCreate]  # Add this field to accept work hours


class Employee(EmployeeBase):
    id: int

    class Config:
        orm_mode = True


class WorkHourBase(BaseModel):
    weekday: str
    start_time: time
    end_time: time


class WorkHour(WorkHourBase):
    id: int
    employee_id: int

    class Config:
        orm_mode = True


class VacationBase(BaseModel):
    vacation_start: date
    vacation_end: date
    type_of_vacation: str
    status: Optional[str] = "pending"


class VacationCreate(BaseModel):
    employee_id: int
    vacation_start: str  # Ensure this matches the expected format
    vacation_end: str  # Ensure this matches the expected format
    type_of_vacation: str


class Vacation(VacationBase):
    id: int
    employee_id: int

    class Config:
        orm_mode = True


class EmployeeLogin(BaseModel):
    email: str
    password: str
