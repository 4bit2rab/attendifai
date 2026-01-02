# main.py
import sys
import sqlite3
import requests
from datetime import date, datetime, timedelta
from PyQt6.QtWidgets import QApplication, QMessageBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from dbConfig import initialize_db,mark_day_as_synced,get_daily_productivity
from tracker import ActivityTracker
from notifications.widget import AttendifAIWidget
from overtime_ui import OvertimeNotification


DB_PATH = "attendance_agent.db"
BACKEND_URL = "http://127.0.0.1:9000"

# ---------------- DATABASE / TOKEN ----------------
def save_token(token: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auth_token (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("INSERT INTO auth_token (token) VALUES (?)", (token,))
    conn.commit()
    conn.close()

def load_token() -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT token FROM auth_token ORDER BY created_at DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if not row:
        #raise RuntimeError("Employee not registered")
        return False
    return row[0]

def register_employee(email: str):
    try:
        response = requests.post(f"{BACKEND_URL}/generate-token", json={"employee_email": email}, timeout=5)
        if response.status_code == 200:
            token = response.json()["token"]
            save_token(token)
            return True, "Employee registered successfully!"
        return False, f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return False, f"Network error: {str(e)}"

# ---------------- REGISTRATION WINDOW ----------------
class RegistrationWindow(QWidget):
    def __init__(self, on_registered_callback):
        super().__init__()
        self.on_registered_callback = on_registered_callback
        self.setWindowTitle("Employee Registration")
        self.setFixedSize(300, 150)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter your email:"))
        self.email_input = QLineEdit()
        layout.addWidget(self.email_input)
        register_btn = QPushButton("Register")
        register_btn.clicked.connect(self.register)
        layout.addWidget(register_btn)
        self.setLayout(layout)

    def register(self):
        email = self.email_input.text().strip()
        if not email:
            QMessageBox.warning(self, "Error", "Please enter your email!")
            return
        success, message = register_employee(email)
        if success:
            QMessageBox.information(self, "Success", message)
            self.close()
            self.on_registered_callback()
        else:
            QMessageBox.critical(self, "Failed", message)

# ---------------- SHIFT FETCH ----------------
def fetch_shift():
    headers = {"Authorization": f"Bearer {load_token()}"}
    response = requests.get(f"{BACKEND_URL}/shift", headers=headers)
    if response.status_code == 200:
        data = response.json()
        shift_code = data["shift_code"]
        start = datetime.strptime(data["shift_start"], "%H:%M:%S").time()
        end = datetime.strptime(data["shift_end"], "%H:%M:%S").time()
        return start, end, shift_code
    raise RuntimeError(f"Failed to fetch shift: {response.text}")

def sync_productivity():
    yesterday_date = date.today() - timedelta(days=1)
    prod, idle, overtime = get_daily_productivity(yesterday_date)
    if prod:
        payload = {
            "log_date": yesterday_date.isoformat(),
            "productive_time": prod,
            "idle_time": idle,
            "over_time": overtime,
        }

        headers = {"Authorization": f"Bearer {load_token()}"}
        response = requests.post(f"{BACKEND_URL}/sync",json=payload, headers=headers)

        if response.status_code == 200:
            mark_day_as_synced(yesterday_date)
            return response.json()

        elif response.status_code == 401:
            raise RuntimeError("Unauthorized - token invalid or expired")

        else:
            raise RuntimeError(
                f"Sync failed [{response.status_code}]: {response.text}"
            )

# ---------------- ACTIVITY THRESHOLD ----------------
def fetch_activity_threshold() -> int:
    
    try:
        token = load_token()
        if not token:
            print("No token found, using default threshold 5s")
            return 5

        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BACKEND_URL}/activity-threshold", headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            idle_threshold = data.get("idle_time_out", 5)
            return idle_threshold
        else:
            print(f"Failed to fetch threshold [{response.status_code}], using default 5s")
            return 5
    except Exception as e:
        print("Error fetching activity threshold, using default 5s:", e)
        return 5



# ---------------- ATTENDANCE APP ----------------
class AttendanceApp:
    def __init__(self):
        start_time, end_time, _ = fetch_shift()
        today = date.today()
        self.shift_start_dt = datetime.combine(today, start_time)
        self.shift_end_dt = datetime.combine(today, end_time)
        if self.shift_end_dt <= self.shift_start_dt:  # handle overnight shifts
            self.shift_end_dt += timedelta(days=1)

        idle_threshold_seconds = fetch_activity_threshold()
        self.tracker = ActivityTracker(self, idle_threshold=idle_threshold_seconds)
        self.tracker.start()

        self.shift_seconds = 0
        self.productive_seconds = 0
        self.break_seconds = 0
        self.idle_seconds = 0
        self.overtime_seconds = 0
        self.shift_over = False
        self.overtime_approved = False

    def tick(self):
        now = datetime.now()
        self.tracker.tick()
        active, idle = self.tracker.get_and_reset_counters()

        if now < self.shift_start_dt:
            return  # shift not started

        # Shift in progress
        if self.shift_start_dt <= now <= self.shift_end_dt:
            self.shift_seconds += active + idle
            self.productive_seconds += active
            self.break_seconds += idle
            self.idle_seconds += idle
            return

        if not self.shift_over:
            self.shift_over = True
            self.show_overtime_popup()
            return
        
        if not self.overtime_approved:
                return

        if self.overtime_approved:
            self.shift_seconds += active
            self.productive_seconds += active
            self.overtime_seconds += active
            self.break_seconds += idle
            self.idle_seconds += idle
            return

    def show_overtime_popup(self):
        if hasattr(self, "overtime_popup") and self.overtime_popup.isVisible():
            return 

        self.overtime_popup = OvertimeNotification()
        self.overtime_popup.approved.connect(self.on_overtime_decision)
        self.overtime_popup.show()

    def on_overtime_decision(self, approved: bool):
        print("Overtime approved:", approved)
        self.overtime_approved = approved

# ---------------- START APP ----------------
def start_attendance_app():
    attendance = AttendanceApp()
    ui = AttendifAIWidget(attendance)
    return ui


def main():
    initialize_db() 
    sync_productivity()
    app = QApplication(sys.argv)
    if load_token():
        # Employee already registered, start app directly
        load_token()
        window = start_attendance_app()
    else:
        # No employee registered, show registration window
        def on_registered():
            nonlocal window
            window = start_attendance_app()

        reg_window = RegistrationWindow(on_registered)
        reg_window.show()
        window = reg_window

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
