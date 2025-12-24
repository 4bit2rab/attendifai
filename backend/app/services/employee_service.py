from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from backend.app.dbmodels.attendancedb import Employee, EmployeeToken
from backend.app.models.models import TokenResponse, EmployeeRequest
from backend.app.core.token_generator import create_employee_token
from datetime import datetime

# Service to create a new employee record
def create_employee_record(db_session, employee_request: EmployeeRequest):
    try:
        new_employee = Employee(
            employee_name=employee_request.employee_name,
            employee_email=employee_request.employee_email,
            employee_phone=employee_request.employee_phone,
            shift_code=employee_request.shift_code
        )

        db_session.add(new_employee)
        db_session.commit()
        db_session.refresh(new_employee)

        return new_employee

    except IntegrityError:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee email already exists"
        )

    except Exception:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create employee"
        )
    
# Service to get all employees
def  get_all_employees(db_session):
    return db_session.query(Employee).all()
   
# Service to get employee details by email
def get_employee_by_email(db_session, email):
    return db_session.query(Employee).filter(Employee.employee_email == email).first()

# Service to generate employee token
def generate_employee_token(db_session, email):
    employee = get_employee_by_email(db_session, email)

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee email not found"
        )
    
    existing_token = db_session.query(EmployeeToken).filter(EmployeeToken.employee_id == employee.employee_id).first()

    if existing_token:
        return TokenResponse(token=existing_token.token, employee_id=employee.employee_id)

    token = create_employee_token(employee.employee_id)

    employee_token = EmployeeToken(employee_id=employee.employee_id, token=token, created_at=str(datetime.utcnow()))
    db_session.add(employee_token)
    db_session.commit()

    response = TokenResponse(token=token, employee_id=employee.employee_id)

    return response

# Service to get tokens of all employees
def get_tokens_of_all_employee(db_session):
    tokens = db_session.query(EmployeeToken).all()
    return tokens


 



