from pydantic import BaseModel, EmailStr

class TokenRequest(BaseModel):
    employee_email: EmailStr

class TokenResponse(BaseModel):
    token: str
    employee_id: str    

    
    class Config:
        from_attributes = True