from fastapi import FastAPI,Query
from backend.app.models.models import ShiftAssignRequest, ShiftResponse, ProductivityPayload, TokenResponse, TokenRequest, EmployeeRequest, EmployeeResponse,AttendanceResponse
from desktop_client.app.storage.store import shift_store
from fastapi import FastAPI, Header, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.mySqlConfig import sessionLocal
from fastapi import Depends, HTTPException, status
from backend.app.services.employee_service import generate_employee_token, create_employee_record, get_all_employees
from backend.app.db.mySqlConfig import Base, engine
from backend.app.dbmodels.attendancedb import EmployeeActivityLog,ShiftDetails,Employee,EmployeeToken
from typing import List
from pydantic import BaseModel
from jose import jwt
import sqlite3
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",  # React dev server
]
SECRET_KEY = "hackathon-secret"
ALGORITHM = "HS256"

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Attendance Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for all origins during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_emp_id(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        print(token)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["employee_id"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
 
 # ---------------- REGISTRATION ----------------
@app.post("/generate-token", response_model=TokenResponse)
def generate_token(
    request: TokenRequest, db: Session = Depends(get_db)
    ):
    response_token = generate_employee_token(db, request.employee_email)
    return response_token
 
# ---------------- GET EMPLOYEE ----------------
@app.post("/sync")
def record_productivity(
    payload: ProductivityPayload, authorization: str = Header(...)
,db: Session = Depends(get_db)):
    employee_id = get_emp_id(authorization)
 
    employee_activity_log = EmployeeActivityLog(employee_id=employee_id,
    log_date=payload.log_date,
    productive_time=payload.productive_time,
    idle_time=payload.idle_time,
    over_time=payload.over_time)
    db.add(employee_activity_log)
    db.commit()
 
    return {
        "success": True,
        "message": "Productivity recorded",
    }


# ---------------- SHIFT ----------------
@app.post("/create-shift")
def assign_shift(
    data: ShiftAssignRequest,
    db: Session = Depends(get_db),
):
    
    shift = ShiftDetails(
        shift_code=data.shift_code,
        shift_start=data.shift_start,
        shift_end=data.shift_end
    )
 
    db.add(shift)
    db.commit()
    db.refresh(shift)
 
    return {
        "success": True,
        "message": "Shift created",
    }

@app.get("/shift", response_model=ShiftResponse)
def get_shift(
    db: Session = Depends(get_db),
    authorization: str = Header(...)
):
    employee_id = get_emp_id(authorization)  

    employee_details = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_id)
        .first()
    )

    shift_details = (
        db.query(ShiftDetails)
        .filter(ShiftDetails.shift_code == employee_details.shift_code)
        .first()
    )
 
    if not shift_details:
        return ShiftResponse(
            shift_code=None,
            shift_start=None,
            shift_end=None,
        )
 
    return shift_details

@app.put("/update-shift-time/{shift_code}", response_model=ShiftResponse)
def update_shift(shift_code: str,
    data: ShiftAssignRequest,
    db: Session = Depends(get_db)
):
    shift = (
        db.query(ShiftDetails)
        .filter(ShiftDetails.shift_code == shift_code)
        .first()
    )
 
    if not shift:
        raise HTTPException(
            status_code=404,
            detail="Shift  does not exist"
        )
 
    if data.shift_end <= data.shift_start:
        raise HTTPException(
            status_code=400,
            detail="Shift end must be after shift start"
        )
 
    shift.shift_start = data.shift_start
    shift.shift_end = data.shift_end
 
    db.commit()
    db.refresh(shift)
 
    return ShiftResponse(
        shift_code=shift_code,
        shift_start=shift.shift_start,
        shift_end=shift.shift_end,
    )

# ---------------- Employee ----------------

# Endpoint to create a new employee
@app.post("/create-employee", response_model=EmployeeResponse, status_code=201)
def create_employee(request: EmployeeRequest, db: Session = Depends(get_db)):
    return create_employee_record(db, request)

@app.put("/assign-shift/{employee_id}")
def update_employee_shift(employee_id,
shift_code: str,
db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee does not exist"
        )

    employee.shift_code = shift_code
    db.commit()
    db.refresh(employee)

    return {
        "success": True,
        "message": "Employee shift updated",
    }

# Endpoint to get all employee details
@app.get("/get-all-employee")
def get_employee(db: Session = Depends(get_db)):
    return get_all_employees(db)

@app.get("/attendance", response_model=List[AttendanceResponse])
def get_attendance(
    date: str= Query(...) ,db: Session = Depends(get_db),
):
    results = (
        db.query(
            Employee.employee_name,
            EmployeeActivityLog.log_date,
            EmployeeActivityLog.productive_time,
            EmployeeActivityLog.idle_time,
            EmployeeActivityLog.over_time,
        )
        .join(
            Employee,
            Employee.employee_id == EmployeeActivityLog.employee_id
        )
        .filter(EmployeeActivityLog.log_date == date)
        .order_by(EmployeeActivityLog.log_date.desc())
        .all()
    )

    if not results:
        return []

    return [
        AttendanceResponse(
            employee_name=row.employee_name,
            log_date=row.log_date,
            productive_time=row.productive_time,
            idle_time=row.idle_time,
            over_time=row.over_time,
        )
        for row in results
    ]

