from pydantic import BaseModel, EmailStr
from datetime import time,date
from typing import Literal,List

class ProductivityPayload(BaseModel):
    log_date: date
    productive_time: int
    idle_time: int
    over_time: int

class TokenRequest(BaseModel):
    employee_email: EmailStr
 
class TokenResponse(BaseModel):
    token: str
    employee_id: str  


class ShiftAssignRequest(BaseModel):
    shift_code: str
    shift_start: time
    shift_end: time

class ShiftResponse(BaseModel):
    shift_code: str
    shift_start: time
    shift_end: time

class EmployeeRequest(BaseModel):
    employee_name: str
    employee_email: EmailStr
    employee_phone: str
    shift_code: str

class AttendanceResponse(BaseModel):
    employee_id:str
    employee_name: str
    log_date: date
    productive_time: int
    idle_time: int
    over_time: int

class EmployeeResponse(BaseModel):
    employee_id: str

class ManagerRequest(BaseModel):
    manager_name: str   
    manager_email: EmailStr
    manager_phone: str
    department: str

class ManagerRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    
class ManagerResponse(BaseModel):
    token: str
    token_type: Literal["Bearer"] = "Bearer"

class ManagerEmployeeMapCreate(BaseModel):
    manager_id: str
    employee_id: str


class ActivityLog(BaseModel):
    log_date: date
    productive_time: int
    idle_time: int
    over_time: int

class EmployeeInput(BaseModel):
    employee_id: str
    employee_name: str
    total_productive_hours: float
    total_overtime_hours: float
    logs: List[ActivityLog] = []


    class Config:   
        from_attributes = True

class ApprovalItem(BaseModel):
    employee_id: str
    log_date: date
    status: str 

class OvertimeApprovalPayload(BaseModel):
    approvals: List[ApprovalItem]

class MonthlySalaryResponse(BaseModel):
    employee_id: str
    employee_name: str
    total_salary: float
    
class ActivityThresholdCreate(BaseModel):
    idle_time_out: int

class ActivityThresholdResponse(BaseModel):
    id: int
    idle_time_out: int
