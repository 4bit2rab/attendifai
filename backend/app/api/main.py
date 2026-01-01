from fastapi import FastAPI,Query, Header, HTTPException,Depends,status
from backend.app.models.models import ManagerRequest, ShiftAssignRequest, ShiftResponse, ProductivityPayload, TokenResponse, TokenRequest, EmployeeRequest, EmployeeResponse, ManagerResponse, ManagerEmployeeMapCreate,ManagerRegisterRequest,AttendanceResponse
from desktop_client.app.storage.store import shift_store
from sqlalchemy.orm import Session
from backend.app.db.mySqlConfig import sessionLocal,Base, engine
from backend.app.services.employee_service import generate_employee_token, create_employee_record, get_all_employees
from backend.app.services.manager_service import assign_employee_to_manager_record, authenticate_manager, create_manager_record, generate_employee_productivity_report
from backend.app.services.manager_service import assign_employee_to_manager_record, authenticate_manager, create_manager_record, generate_employee_productivity_report, update_manager_password
from backend.app.db.mySqlConfig import Base, engine
from backend.app.dbmodels.attendancedb import EmployeeActivityLog,ShiftDetails,Employee,EmployeeToken
from typing import List
from backend.app.dbmodels.attendancedb import EmployeeActivityLog, ManagerEmployeeMap,ShiftDetails,Employee,Manager
from datetime import date
from backend.app.core.security import hash_password
from pydantic import BaseModel
from jose import jwt
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.token_generator import get_user_id

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

@app.delete("/delete-shift/{shift_code}")
def delete_shift(
    shift_code: str,
    db: Session = Depends(get_db),
):
    shift = db.query(ShiftDetails).filter(ShiftDetails.shift_code == shift_code).first()
    if not shift:
        raise HTTPException(status_code=404, detail="Shift not found")
    db.delete(shift)
    db.commit()

@app.get("/shifts", response_model=List[ShiftResponse])
def get_shifts(
    db: Session = Depends(get_db),
):
    results = (
        db.query(
            ShiftDetails.shift_code,
            ShiftDetails.shift_start,
            ShiftDetails.shift_end,
        ).all()
    )

    return [
        ShiftResponse(
            shift_code=row.shift_code,
            shift_start=row.shift_start,
            shift_end=row.shift_end,
        )
        for row in results
    ]


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
    # employee_ids = (
    #     db.query(ManagerEmployeeMap.employee_id)
    #     .filter(ManagerEmployeeMap.manager_id == current_manager_id)
    #     .all()
    # )
    # employee_ids = [eid[0] for eid in employee_ids]

    # if not employee_ids:
    #     return []
    # logs = (
    #     db.query(EmployeeActivityLog)
    #     .filter(EmployeeActivityLog.employee_id.in_(employee_ids))
    #     .all()
    # )
    # response = []
    # employees = db.query(Employee).filter(Employee.employee_id.in_(employee_ids)).all()
    # emp_map = {emp.employee_id: emp.employee_name for emp in employees}

    # for log in logs:
    #     response.append(
    #         AttendanceResponse(
    #             employee_name=emp_map.get(log.employee_id, "Unknown"),
    #             log_date=log.log_date,
    #             productive_time=log.productive_time,
    #             idle_time=log.idle_time,
    #             over_time=log.over_time,
    #         )
    #     )

    # return response
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



# ---------------- Manager ----------------
# Endpoint to create a new manager  
@app.post("/create-manager", response_model=ManagerResponse, status_code=201)
def create_manager(request: ManagerRequest, db: Session = Depends(get_db)):
    return create_manager_record(db, request)

# Endpoint for manager login
@app.get("/manager/login", response_model=ManagerResponse)
def login_manager(email: str, password: str, db: Session = Depends(get_db)):
    return authenticate_manager(db, email, password)

@app.post("/manager/register", response_model=ManagerResponse)
def register_manager(request: ManagerRegisterRequest, db: Session = Depends(get_db)):
    manager = db.query(Manager).filter(Manager.manager_email == request.email).first()
    if not manager:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is not registered as a manager"
        )
    manager.password_hash = hash_password(request.password)
    db.add(manager)
    db.commit()
    db.refresh(manager)
    return ManagerResponse(manager_id=manager.manager_id)

# ---------------- Manager Employee Mapping ----------------
@app.post("/assign-employee")
def assign_employee_to_manager(request: ManagerEmployeeMapCreate, db: Session = Depends(get_db)):
    return assign_employee_to_manager_record(db, request)

@app.get("/manager/employees")
def get_employees(authorization: str = Header(...), db: Session = Depends(get_db)):
    manager_id = get_user_id(authorization)
    print("Manager ID:", manager_id)
    data = db.query(ManagerEmployeeMap).filter(
        ManagerEmployeeMap.manager_id == manager_id
    ).all()

    return {
        "manager_id": manager_id,
        "employees": [
            {
                "employee_id": m.employee.employee_id,
                "employee_name": m.employee.employee_name,
                "employee_email": m.employee.employee_email,
                "employee_phone": m.employee.employee_phone,
                "shift_code": m.employee.shift_code,
            }
            for m in data
        ]
    }

@app.get("/employee/report")
def get_employee_report(manager_id: str, start_date: date | None = Query(None), end_date: date | None = Query(None), db: Session = Depends(get_db)):
    return  generate_employee_productivity_report(db, manager_id, start_date, end_date)

@app.put("/register/manger")
def register_manager(manager_email: str, password: str, db: Session = Depends(get_db)):
    return update_manager_password(db,manager_email,password)
 