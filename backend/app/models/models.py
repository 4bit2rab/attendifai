from pydantic import BaseModel, EmailStr
from datetime import time,date


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
    password_hash: str

class ManagerResponse(BaseModel):
    manager_id: str

from pydantic import BaseModel

class ManagerEmployeeMapCreate(BaseModel):
    manager_id: str
    employee_id: str
    

    class Config:   
        from_attributes = True