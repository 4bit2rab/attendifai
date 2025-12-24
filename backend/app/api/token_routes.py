from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.token import TokenRequest, TokenResponse
from app.dbConfig.mysqlConfig import sessionLocal
from app.services.employee_service import generate_employee_token, get_tokens_of_all_employee
from app.core.decode_token import get_employee_id_from_token

router = APIRouter()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to generate employee token
@router.post("/generate-token", response_model=TokenResponse)
def generate_token(request: TokenRequest, db: Session = Depends(get_db)):
        response_token = generate_employee_token(db, request.employee_email)
        return response_token

# Endpoint to get tokens of all employees
@router.get("/get-all-tokens")
def get_all_tokens(db: Session = Depends(get_db)):
    return get_tokens_of_all_employee(db)

@router.get("/employee-id")
def get_employee_id(employee_id: int = Depends(get_employee_id_from_token)):
     return {"employee_id": employee_id}

