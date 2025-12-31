from sqlalchemy import Column, Integer, String, Time, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.app.db.mySqlConfig import Base
import uuid

# Database model for Employee
class Employee(Base):
    __tablename__ = "employee"

    employee_id = Column(String(50), primary_key=True, index=True, default= lambda: str(uuid.uuid4()))
    employee_name = Column(String(100), index=True)
    employee_email = Column(String(100), unique=True, index=True)
    employee_phone = Column(String(20), unique=True, index=True, nullable=False)
    shift_code = Column(String(30),nullable=False)

    managers = relationship(
    "ManagerEmployeeMap",
    back_populates="employee",
    cascade="all, delete"
    )


# Database model for EmployeeToken
class EmployeeToken(Base):
    __tablename__ = "employee_token"

    token = Column(String(255), primary_key=True, index=True)
    employee_id = Column(String(50), index=True)
    created_at = Column(String(100))

# Database model for ShiftDetails
class ShiftDetails(Base):
    __tablename__ = "shift_details"

    shift_code = Column(String(30), primary_key=True, index=True)
    shift_start = Column(Time,nullable=False)
    shift_end = Column(Time,nullable=False)

class EmployeeActivityLog(Base):
    __tablename__ = "employee_activity_log"

    employee_id = Column(String(50),nullable=False,primary_key=True)
    log_date = Column(Date,nullable=False,primary_key=True)
    productive_time = Column(Integer,nullable=False,default=0)
    idle_time = Column(Integer,nullable=False,default=0)
    over_time = Column(Integer,nullable=False,default=0)

# Database model for manager details
class Manager(Base):
    __tablename__ = "manager_details"

    manager_id = Column(String(50), primary_key=True, index=True, default= lambda: str(uuid.uuid4()))
    manager_name = Column(String(100), index=True)  
    manager_email = Column(String(100), unique=True, index=True, nullable=False)
    manager_phone = Column(String(20), unique=True, index=True, nullable=False)
    department = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=True)

    employees = relationship(
    "ManagerEmployeeMap",
    back_populates="manager",
    cascade="all, delete"
    )

# Database model for mapping between Manager and Employee
class ManagerEmployeeMap(Base):
    __tablename__ = "manager_employee_map"

    id = Column(Integer, primary_key=True)
    manager_id = Column(String(50), ForeignKey("manager_details.manager_id"), nullable=False)
    employee_id = Column(String(50), ForeignKey("employee.employee_id"), nullable=False)

    manager = relationship("Manager", back_populates="employees")
    employee = relationship("Employee", back_populates="managers")

    __table_args__ = (
        UniqueConstraint("manager_id", "employee_id", name="uq_manager_employee"),
    )


