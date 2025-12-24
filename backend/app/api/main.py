from fastapi import FastAPI
from backend.app.models.models import ShiftAssignRequest, ShiftResponse, ProductivityPayload, TokenResponse, TokenRequest
from desktop_client.app.storage.store import shift_store
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from jose import jwt
SECRET_KEY = "hackathon-secret"
ALGORITHM = "HS256"

app = FastAPI(title="Attendance Backend")

def get_emp_id(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["emp_id"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
 
 # ---------------- REGISTRATION ----------------
@app.post("/generate-token", response_model=TokenResponse)
def generate_token(
    request: TokenRequest, db: Session = Depends(get_db)
    ):
    response_token = generate_employee_token(db, request.employee_email)
    return response_token
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

def create_employee_token(employee_id: int):
 
    to_encode = {"employee_id": employee_id}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

 
 
# ---------------- GET EMPLOYEE ----------------
@app.post("/sync", response_model=ProductivityPayload)
def record_productivity(
    payload: ProductivityPayload, authorization: str = Header(...)
):
    emp_id = get_emp_id(authorization)
 
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO productivity (emp_id, date, productive_seconds, idle_seconds)
        VALUES (?, ?, ?, ?)
    """,
        (
            emp_id,
            payload.date,
            payload.productive_seconds,
            payload.idle_seconds,
        ),
    )
    conn.commit()
    conn.close()
 
    return {
        "success": True,
        "message": "Productivity recorded",
    }


# ---------------- SHIFT ----------------
@app.post("/assign-shift", response_model=ShiftResponse)
def assign_shift(data: ShiftAssignRequest):
    shift_store[data.employee_id] = {
        "start": data.shift_start,
        "end": data.shift_end
    }
    return ShiftResponse(
        employee_id=data.employee_id,
        shift_start=data.shift_start,
        shift_end=data.shift_end,
        status="assigned"
    )


@app.get("/shift/{employee_id}", response_model=ShiftResponse)
def get_shift(employee_id: str):
    shift = shift_store.get(employee_id)
    if not shift:
        return ShiftResponse(
            employee_id=employee_id,
            shift_start="",
            shift_end="",
            status="not found"
        )

    return ShiftResponse(
        employee_id=employee_id,
        shift_start=shift["start"],
        shift_end=shift["end"],
        status="found"
    )
