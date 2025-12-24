import sys
import requests
import sqlite3
from datetime import date, timedelta, datetime
from dbConfig import initialize_db

from PyQt6.QtWidgets import (
    QApplication, QMessageBox, QLabel, QVBoxLayout, QWidget
)
from PyQt6.QtCore import QTimer

from tracker import ActivityTracker
from tracker_widget import TrackerWindow

DB_PATH = "attendance_agent.db"


# ---------------- User Registration ----------------
def register_employee(employee_email):
    response = requests.post(
        "http://127.0.0.1:8000/generate-token",
        json={"employee_email": employee_email}
    )
    data = response.json()
    if response.status_code == 200:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
                INSERT INTO auth_token (token, created_at)
                VALUES (?, datetime('now'))
            """,
            (data["token"],),
        )
        conn.commit()
        conn.close()


# ---------------- FETCH SHIFT FROM API ----------------
def fetch_shift():

    headers = {
    "Authorization": f"Bearer {load_token()}",
    "Content-Type": "application/json",
}
    response = requests.get("http://127.0.0.1:8000/shift", headers=headers)


    if response.status_code == 200:
        data = response.json()
        shift_code = data["shift_code"]
        start = datetime.strptime(data["shift_start"], "%H:%M:%S").time()
        end = datetime.strptime(data["shift_end"], "%H:%M:%S").time()
        return start, end , shift_code

# ---------------- Productivity sync ----------------
def sync_productivity():
    API_URL = "http://127.0.0.1:8000/sync"
 
    yesterday_date = date.today() - timedelta(days=1)
    prod, idle, overtime = get_daily_productivity(yesterday_date)
    if prod:
        payload = {
            "log_date": yesterday_date.isoformat(),
            "productive_time": prod,
            "idle_time": idle,
            "over_time": overtime
        }
 
        headers = {
            "Authorization": f"Bearer {load_token()}",
            "Content-Type": "application/json",
        }
 
        response = requests.post(
            API_URL, json=payload, headers=headers, timeout=10
        )
 
        if response.status_code == 200:
            mark_day_as_synced(yesterday_date)
            return response.json()
 
        elif response.status_code == 401:
            raise RuntimeError("Unauthorized - token invalid or expired")
 
        else:
            raise RuntimeError(
                f"Sync failed [{response.status_code}]: {response.text}"
            )
 
 

def load_token() -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
 
    cursor.execute(
        """
        SELECT token
        FROM auth_token
        ORDER BY created_at DESC
        LIMIT 1
    """
    )
 
    row = cursor.fetchone()
    conn.close()
 
    if not row:
        raise RuntimeError("No token found. Employee not registered.")
 
    return row[0]

def mark_day_as_synced(date_str: date):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
 
    cursor.execute(
        """
        UPDATE employee_activity
        SET synced = 1
        WHERE date = ?
    """,
        (date_str.isoformat(),),
    )
 
    conn.commit()
    conn.close()
 
def get_daily_productivity(target_date: date):
 
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
 
    cursor.execute(
        """
        SELECT type, start_time, end_time
        FROM employee_activity
        WHERE date = ? AND synced = 0 AND overtime=0
    """,
        (target_date.isoformat(),),
    )
 
    productive_seconds = 0
    idle_seconds = 0
 
    for session_type, start, end in cursor.fetchall():
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
        duration = max(0, int((end_dt - start_dt).total_seconds()))
 
        if session_type == "productive":
            productive_seconds += duration
        else:
            idle_seconds += duration
 
    cursor.execute(
        """
        SELECT start_time, end_time
        FROM employee_activity
        WHERE date = ?
        AND synced = 0
        AND overtime = 1
        AND type = 'productive'
        """,
        (target_date.isoformat(),),
    )
    overtime_productive_seconds = 0
 
    for start, end in cursor.fetchall():
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
        overtime_productive_seconds += max(
            0, int((end_dt - start_dt).total_seconds())
        )
 
    conn.close()
 
    return productive_seconds, idle_seconds, overtime_productive_seconds
 
 

# ---------------- OVERTIME POPUP ----------------
def ask_overtime(worked_minutes):
    msg = QMessageBox()
    msg.setWindowTitle("Overtime Detected")

    container = QWidget(msg)
    layout = QVBoxLayout(container)

    info = QLabel(
        f"You worked {worked_minutes} minutes.\n"
        "Do you want to continue as overtime?"
    )

    timer_label = QLabel("00:00")
    timer_label.setStyleSheet("font-size:18px;font-weight:bold")

    layout.addWidget(info)
    layout.addWidget(timer_label)
    msg.layout().addWidget(container)

    msg.setStandardButtons(
        QMessageBox.StandardButton.Yes |
        QMessageBox.StandardButton.No
    )

    start_time = datetime.now()
    timer = QTimer(msg)

    def update_timer():
        elapsed = int((datetime.now() - start_time).total_seconds())
        m, s = divmod(elapsed, 60)
        timer_label.setText(f"{m:02d}:{s:02d}")

    timer.timeout.connect(update_timer)
    timer.start(1000)

    result = msg.exec()
    timer.stop()

    return result == QMessageBox.StandardButton.Yes


# ---------------- MAIN ATTENDANCE LOGIC ----------------
class AttendanceApp:
    def __init__(self, employee_id):
        self.employee_id = employee_id

        start_time, end_time = fetch_shift(employee_id)
        today = date.today()

        self.shift_start_dt = datetime.combine(today, start_time)
        self.shift_end_dt = datetime.combine(today, end_time)

        self.shift_start = start_time.strftime("%H:%M")
        self.shift_end = end_time.strftime("%H:%M")

        self.tracker = ActivityTracker(idle_threshold=10)
        self.tracker.start()

        self.shift_seconds = 0
        self.productive_seconds = 0
        self.break_seconds = 0

        self.shift_over = False
        self.overtime_approved = False

    def tick(self):
        now = datetime.now()

        if now < self.shift_start_dt:
            return

        if self.shift_start_dt <= now <= self.shift_end_dt:
            self.tracker.tick()
            self.shift_seconds += 1
            self.productive_seconds += self.tracker.active_seconds
            self.break_seconds += self.tracker.break_seconds
            self.tracker.reset()
            return

        if now > self.shift_end_dt:
            if not self.shift_over:
                self.shift_over = True
                worked_minutes = self.shift_seconds // 60
                self.overtime_approved = ask_overtime(worked_minutes)

            if self.overtime_approved:
                self.shift_seconds += 1
                self.productive_seconds += 1


# ---------------- APP START ----------------
def main():
    app = QApplication(sys.argv)  # ✅ FIRST LINE

    attendance = AttendanceApp("EMP001")
    window = TrackerWindow(attendance)
    window.show()

    timer = QTimer()
    timer.timeout.connect(attendance.tick)
    timer.start(1000)

    sys.exit(app.exec())

if __name__ == "__main__":
    initialize_db()
    main()