from fastapi import FastAPI
from .database import get_minute_activity_logs, get_overtime_logs

app = FastAPI(
    title="Attendance Tracker API",
    description="API to view employee activity and overtime logs",
    version="1.0"
)

# ---- Endpoints ----

@app.get("/activity", tags=["Activity"])
def read_activity_logs():
    """
    Get all minute-by-minute activity logs.
    """
    return get_minute_activity_logs()


@app.get("/overtime", tags=["Overtime"])
def read_overtime_logs():
    """
    Get all overtime logs.
    """
    return get_overtime_logs()
