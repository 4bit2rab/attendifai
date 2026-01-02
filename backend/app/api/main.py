from fastapi import FastAPI,Query, Header, HTTPException,Depends,status
from backend.app.models.models import ManagerRequest, ShiftAssignRequest, ShiftResponse, ProductivityPayload, TokenResponse, TokenRequest, EmployeeRequest, EmployeeResponse, ManagerResponse, ManagerEmployeeMapCreate,ManagerRegisterRequest,AttendanceResponse,OvertimeApprovalPayload, ActivityThresholdCreate, ActivityThresholdResponse,MonthlySalaryResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.app.db.mySqlConfig import sessionLocal,Base, engine
from backend.app.services.employee_service import generate_employee_token, create_employee_record, get_all_employees
from backend.app.services.manager_service import assign_employee_to_manager_record, authenticate_manager, calculate_total_productivity, create_manager_record, generate_employee_productivity_report, update_manager_password
from typing import List
from backend.app.dbmodels.attendancedb import EmployeeActivityLog, ManagerEmployeeMap,ShiftDetails,Employee,Manager,EmployeeBaseSalary, ActivityThreshold
from datetime import date
from backend.app.dbmodels.attendancedb import EmployeeActivityLog, ManagerEmployeeMap,ShiftDetails,Employee,Manager
from datetime import date, timedelta
from backend.app.core.security import hash_password
from jose import jwt
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.token_generator import get_user_id
from backend.app.ai.features import extract_employee_features
from backend.app.ai.predictor import predict_next_week_productivity
from backend.app.ai.employee_ranking import rank_employees_ai
from backend.app.models.models import EmployeeInput

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
    emp_salary = (
        db.query(EmployeeBaseSalary)
        .filter(EmployeeBaseSalary.employee_id == employee_id)
        .first()
    )
    hourly_salary = emp_salary.hourly_salary if emp_salary else 0
    hours_worked = payload.productive_time / 3600
    per_day_salary = hourly_salary * hours_worked

    employee_activity_log = EmployeeActivityLog(employee_id=employee_id,
    log_date=payload.log_date,
    productive_time=payload.productive_time,
    idle_time=payload.idle_time,
    over_time=payload.over_time,
    per_day_base_salary=per_day_salary)
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
    date: str= Query(...) ,authorization: str = Header(...),db: Session = Depends(get_db),
):
    manager_id = get_user_id(authorization)
    results = (
        db.query(
            Employee.employee_id,
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
        .join(
            ManagerEmployeeMap,
            ManagerEmployeeMap.employee_id == Employee.employee_id
        )
        .filter(
            ManagerEmployeeMap.manager_id == manager_id,
            EmployeeActivityLog.log_date == date
        )
        .order_by(EmployeeActivityLog.log_date.desc())
        .all()
    )

    if not results:
        return []

    return [
        AttendanceResponse(
            employee_id=row.employee_id,
            employee_name=row.employee_name,
            log_date=row.log_date,
            productive_time=row.productive_time,
            idle_time=row.idle_time,
            over_time=row.over_time,
        )
        for row in results
    ]

@app.get("/overtime")
def get_overtime(
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):
    manager_id = get_user_id(authorization)

    results = (
        db.query(
            Employee.employee_id,
            Employee.employee_name,
            EmployeeActivityLog.log_date,
            EmployeeActivityLog.over_time,
            EmployeeActivityLog.overtime_approval,
        )
        .join(Employee, Employee.employee_id == EmployeeActivityLog.employee_id)
        .join(ManagerEmployeeMap, ManagerEmployeeMap.employee_id == Employee.employee_id)
        .filter(
            ManagerEmployeeMap.manager_id == manager_id,
            EmployeeActivityLog.over_time > 0,
            EmployeeActivityLog.overtime_approval == 0
        )
        .order_by(EmployeeActivityLog.log_date)
        .all()
    )

    return [
        {
            "employee_id": row.employee_id,
            "employee_name": row.employee_name,
            "log_date": row.log_date,
            "over_time": row.over_time,
        }
        for row in results
    ]


# ---------------- Manager ---------------
# Endpoint to create a new manager  
@app.post("/create-manager", status_code=201)
def create_manager(request: ManagerRequest, db: Session = Depends(get_db)):
    return create_manager_record(db, request)

# Endpoint for manager login
@app.get("/manager/login", response_model=ManagerResponse)
def login_manager(email: str, password: str, db: Session = Depends(get_db)):
    return authenticate_manager(db, email, password)

@app.post("/manager/register")
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
    return manager

# Get manager details
@app.get("/manager/details")
def get_manager_details(authorization: str = Header(...), db: Session = Depends(get_db)):
    manager_id = get_user_id(authorization)
    manager = db.query(Manager).filter(Manager.manager_id == manager_id).first()
    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manager not found"
        )
    return {
        "manager_id": manager.manager_id,
        "manager_name": manager.manager_name
    }

# ---------------- Manager Employee Mapping ----------------
@app.post("/assign-employee")
def assign_employee_to_manager(request: ManagerEmployeeMapCreate, db: Session = Depends(get_db)):
    return assign_employee_to_manager_record(db, request)

@app.get("/manager/employees")
def get_employees(authorization: str = Header(...), db: Session = Depends(get_db)):
    manager_id = get_user_id(authorization)
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
def get_employee_report(authorization: str = Header(...), start_date: date | None = Query(None), end_date: date | None = Query(None), db: Session = Depends(get_db)):
    manager_id = get_user_id(authorization)
    return  generate_employee_productivity_report(db, manager_id, start_date, end_date)

@app.get("/report", response_model=List[AttendanceResponse])
def get_monthly_report(
    authorization: str = Header(...),
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
):
    manager_id = get_user_id(authorization)
    start_date = date(year, month, 1)

    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)
    results = (
        db.query(
            Employee.employee_id,
            Employee.employee_name,
            EmployeeActivityLog.log_date,
            EmployeeActivityLog.productive_time,
            EmployeeActivityLog.idle_time,
            EmployeeActivityLog.over_time,
        )
        .join(
            ManagerEmployeeMap,
            ManagerEmployeeMap.employee_id == Employee.employee_id
        )
        .join(
            EmployeeActivityLog,
            EmployeeActivityLog.employee_id == Employee.employee_id
        )
        .filter(
            ManagerEmployeeMap.manager_id == manager_id,
            EmployeeActivityLog.log_date >= start_date,
            EmployeeActivityLog.log_date < end_date,
        )
        .order_by(
            Employee.employee_name,
            EmployeeActivityLog.log_date
        )
        .all()
    )

    return results



@app.get("/report/salary", response_model=List[MonthlySalaryResponse])
def get_monthly_salary(
    authorization: str = Header(...),
    year: int = Query(..., ge=2000),
    month: int = Query(..., ge=1, le=12),
    db: Session = Depends(get_db),
):
    manager_id = get_user_id(authorization)

    start_date = date(year, month, 1)
    end_date = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)

    # Sum per_day_base_salary grouped by employee
    results = (
        db.query(
            Employee.employee_id,
            Employee.employee_name,
            func.sum(EmployeeActivityLog.per_day_base_salary).label("total_salary")
        )
        .join(EmployeeActivityLog, EmployeeActivityLog.employee_id == Employee.employee_id)
        .join(ManagerEmployeeMap, ManagerEmployeeMap.employee_id == Employee.employee_id)
        .filter(
            ManagerEmployeeMap.manager_id == manager_id,
            EmployeeActivityLog.log_date >= start_date,
            EmployeeActivityLog.log_date < end_date,
        )
        .group_by(Employee.employee_id, Employee.employee_name)
        .all()
    )

    return [
        {
            "employee_id": row.employee_id,
            "employee_name": row.employee_name,
            "total_salary": float(row.total_salary or 0)
        }
        for row in results
    ]

@app.put("/register/manger")
def register_manager(manager_email: str, password: str, db: Session = Depends(get_db)):
    return update_manager_password(db,manager_email,password)

@app.post("/predict-productivity")
def predict_productivity(authorization: str = Header(...), db: Session = Depends(get_db)):
    manager_id = get_user_id(authorization)
    end_date = date.today()
    start_date = end_date - timedelta(days=7)
    report = generate_employee_productivity_report(db, manager_id, start_date, end_date)

    results = []
    for emp in report:
        features = extract_employee_features(emp)

        if not features:
            results.append({
                "employee_id": emp["employee_id"],
                "employee_name": emp["employee_name"],
                "predicted_next_week_productive_hours": 0,
                "confidence": "Low"
            })
            continue

        predicted = predict_next_week_productivity(features)

        results.append({
            "employee_id": emp["employee_id"],
            "employee_name": emp["employee_name"],
            "predicted_next_week_productive_hours": predicted,
            "confidence": "Medium"
        })

    return results

@app.get("/employee-ranking")
def employee_ranking(authorization: str = Header(...), start_date: date | None = Query(None), end_date: date | None = Query(None), db: Session = Depends(get_db)):
    manager_id = get_user_id(authorization)
    data = generate_employee_productivity_report(db, manager_id, start_date, end_date)

    employees: List[EmployeeInput] = [
        EmployeeInput(**emp) for emp in data
    ]

    rankings = rank_employees_ai(employees)

    # return ranked_df.to_dict(orient="records")
    return {
        "status": "success",
        "manager_id": manager_id,
        "date_range": {
            "start_date": start_date,
            "end_date": end_date
        },
        "rankings": rankings
    }

@app.post("/overtime/approve")
def approve_overtime(
    payload: OvertimeApprovalPayload,
    db: Session = Depends(get_db)
):
    for item in payload.approvals:
        record = (
            db.query(EmployeeActivityLog)
            .filter(
                EmployeeActivityLog.employee_id == item.employee_id,
                EmployeeActivityLog.log_date == item.log_date
            )
            .first()
        )

        if not record:
            continue

        record.overtime_approval = True if item.status == "approved" else False
        emp_salary = (
            db.query(EmployeeBaseSalary)
            .filter(EmployeeBaseSalary.employee_id == record.employee_id)
            .first()
        )
        hourly_salary = emp_salary.hourly_salary if emp_salary else 0
        over_hours_worked = record.over_time / 3600
        over_time_salary = hourly_salary * over_hours_worked
        record.per_day_base_salary=record.per_day_base_salary + over_time_salary
    db.commit()

    return {
        "success": True,
        "message": "Overtime approvals updated successfully"
    }
    
@app.post("/activity-threshold", response_model=ActivityThresholdResponse)
def create_or_update_activity_threshold(
    payload: ActivityThresholdCreate,
    db: Session = Depends(get_db)
):
    threshold = db.query(ActivityThreshold).first()
    if threshold:
        # Update existing
        threshold.idle_time_out = payload.idle_time_out
    else:
        # Create new
        threshold = ActivityThreshold(idle_time_out=payload.idle_time_out)
        db.add(threshold)
    db.commit()
    db.refresh(threshold)
    return threshold

@app.put("/activity-threshold/{threshold_id}", response_model=ActivityThresholdResponse)
def update_activity_threshold(
    threshold_id: int,
    payload: ActivityThresholdCreate,
    db: Session = Depends(get_db)
):
    threshold = db.query(ActivityThreshold).filter(ActivityThreshold.id == threshold_id).first()
    if not threshold:
        raise HTTPException(status_code=404, detail="Threshold not found")
    
    threshold.idle_time_out = payload.idle_time_out
    db.commit()
    db.refresh(threshold)
    return threshold

@app.get("/activity-threshold")
def get_activity_threshold(db: Session = Depends(get_db)):

    threshold = db.query(ActivityThreshold).first()
    if threshold:
        return {"idle_time_out": threshold.idle_time_out}
    return {"idle_time_out": 5}  # default

@app.get("/weekly/productivity-summary")
def weekly_productivity_summary(authorization: str = Header(...), db: Session = Depends(get_db)):
    manager_id = get_user_id(authorization)
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)
    data = generate_employee_productivity_report(db, manager_id, start_of_week, end_of_week)

    employees: List[EmployeeInput] = [
        EmployeeInput(**emp) for emp in data
    ]

    response = calculate_total_productivity(employees)

    return response