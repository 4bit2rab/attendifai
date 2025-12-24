from pydantic import BaseModel, EmailStr

class EmployeeRequest(BaseModel):
    employee_name: str
    employee_email: EmailStr

class EmployeeResponse(BaseModel):
    employee_id: str
     

    class Config:   
        from_attributes = True