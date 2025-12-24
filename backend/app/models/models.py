from pydantic import BaseModel, EmailStr
from datetime import time


class ProductivityPayload(BaseModel):
    date: str
    productive_seconds: int
    idle_seconds: int

class TokenRequest(BaseModel):
    employee_email: EmailStr
 
class TokenResponse(BaseModel):
    token: str
    employee_id: str  


class ShiftAssignRequest(BaseModel):
    employee_id: str
    shift_start: time
    shift_end: time

class ShiftResponse(BaseModel):
    employee_id: str
    shift_start: time
    shift_end: time
