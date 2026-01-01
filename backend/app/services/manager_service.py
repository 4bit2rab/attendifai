from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from backend.app.core.security import hash_password, verify_password, verify_password
from backend.app.dbmodels.attendancedb import EmployeeActivityLog, Manager, ManagerEmployeeMap
from backend.app.models.models import ManagerRequest
from datetime import date, timedelta
from sqlalchemy import func
from collections import defaultdict
from backend.app.core.token_generator import create_employee_token

# Service to create a new manager record
def create_manager_record(db_session, manager_request: ManagerRequest):
    try:
        hashed_pwd = hash_password(manager_request.password_hash)
        new_manager = Manager(
            manager_name=manager_request.manager_name,
            manager_email=manager_request.manager_email,
            manager_phone=manager_request.manager_phone,
            department=manager_request.department,
            password_hash=hashed_pwd
        )

        db_session.add(new_manager)
        db_session.commit()
        db_session.refresh(new_manager)

        return new_manager

    except IntegrityError:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Manager email already exists"
        )

    except Exception:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create manager"
        )

# Service to get manager by email
def authenticate_manager(db, email: str, password: str):
    manager = get_manager_by_email(db, email)

    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No manager found with the provided email"
        )

    if not verify_password(password, manager.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    token = create_employee_token(manager.manager_id)

    return {"token": token}

# Service to get manager by email
def get_manager_by_email(db_session, email: str):
    return db_session.query(Manager).filter(Manager.manager_email == email).first()

def assign_employee_to_manager_record(db_session, mapping_request):

     # check if already mapped
    existing = db_session.query(ManagerEmployeeMap).filter(
        ManagerEmployeeMap.manager_id == mapping_request.manager_id,
        ManagerEmployeeMap.employee_id == mapping_request.employee_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Employee already assigned")

    mapping = ManagerEmployeeMap(
        manager_id=mapping_request.manager_id,
        employee_id=mapping_request.employee_id
    )

    db_session.add(mapping)
    db_session.commit()
    db_session.refresh(mapping)


# Service to generate employee productivity report
def generate_employee_productivity_report(db_session, manager_id: str, start_date: date | None = None, end_date: date | None = None):

    # Default date logic
    today = date.today()
    end_date = end_date or today
    start_date = start_date or (end_date - timedelta(days=30))

    # Fetch employees under the manager
    employee_mappings = db_session.query(ManagerEmployeeMap).filter(
        ManagerEmployeeMap.manager_id == manager_id
    ).all()

    # Fetch productivity logs for these employees
    employee_ids = [mapping.employee_id for mapping in employee_mappings]
    
    query = db_session.query(EmployeeActivityLog).filter(
        EmployeeActivityLog.employee_id.in_(employee_ids)
    )

    if start_date:
        query = query.filter(EmployeeActivityLog.log_date >= start_date)
    if end_date:
        query = query.filter(EmployeeActivityLog.log_date <= end_date)

    results = query.all()

    # Calculate total productive time per employee
    total_prodctivity_results = (
        db_session.query(
            EmployeeActivityLog.employee_id,
            func.sum(EmployeeActivityLog.productive_time).label("total_seconds")
        )
        .filter(
            EmployeeActivityLog.employee_id.in_(employee_ids),
            EmployeeActivityLog.log_date.between(start_date, end_date)
        )
        .group_by(EmployeeActivityLog.employee_id)
        .all()
    )

    employee_total_map = {
        row.employee_id: round(row.total_seconds / 3600, 2)
        for row in total_prodctivity_results
    }

    employee_logs_map = defaultdict(list)

    for log in results:
        employee_logs_map[log.employee_id].append({
            "log_date": log.log_date,
            "productive_time": log.productive_time,
            "idle_time": log.idle_time,
            "over_time": log.over_time
        })

    report = []

    for employee_id in employee_ids:
        report.append({
            "employee_id": employee_id,
            "total_productive_hours": employee_total_map.get(employee_id, 0),
            "logs": employee_logs_map.get(employee_id, [])
        })


    return report

def update_manager_password(db_session, manager_email: str, new_password: str):
    manager = get_manager_by_email(db_session, manager_email)
    if not manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manager not found"
        )

    hashed_pwd = hash_password(new_password)
    manager.password_hash = hashed_pwd

    db_session.commit()
    db_session.refresh(manager)

    return {"message": "Password updated successfully"}
