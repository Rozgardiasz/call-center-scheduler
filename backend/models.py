from sqlalchemy import Column, Integer, String, Time, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)

    work_hours = relationship("WorkHour", back_populates="employee")
    vacations = relationship("Vacation", back_populates="employee")

class WorkHour(Base):
    __tablename__ = "work_hours"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    weekday = Column(String, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    employee = relationship("Employee", back_populates="work_hours")

class Vacation(Base):
    __tablename__ = "vacations"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    vacation_start = Column(Date, nullable=False)
    vacation_end = Column(Date, nullable=False)
    type_of_vacation = Column(String, nullable=False)
    status = Column(String(20), default="pending")

    employee = relationship("Employee", back_populates="vacations")
