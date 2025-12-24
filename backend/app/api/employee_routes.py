from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.employee import EmployeeRequest, EmployeeResponse
from app.models.employee import Employee
from app.dbConfig.mysqlConfig import sessionLocal
from app.services.employee_service import create_employee_record, get_all_employees

router = APIRouter()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()  

# Endpoint to create a new employee
@router.post("/create-employee", response_model=EmployeeResponse, status_code=201)
def create_employee(request: EmployeeRequest, db: Session = Depends(get_db)):
    return create_employee_record(db, request)

# Endpoint to get all employee details
@router.get("/get-all-employee")
def get_employee(db: Session = Depends(get_db)):
    return get_all_employees(db)

