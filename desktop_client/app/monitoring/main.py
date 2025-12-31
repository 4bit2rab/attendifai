# main.py
import sys
import sqlite3
import requests
from datetime import date, datetime, timedelta
from PyQt6.QtWidgets import QApplication, QMessageBox, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
from dbConfig import initialize_db
from tracker import ActivityTracker
from tracker_widget import TrackerWindow
from overtime_ui import ask_overtime
from notifications.widget import AttendifAIWidget


DB_PATH = "attendance_agent.db"
BACKEND_URL = "http://127.0.0.1:8000"

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

# ---------------- ATTENDANCE APP ----------------
class AttendanceApp:
    def __init__(self):
        start_time, end_time, _ = fetch_shift()
        today = date.today()
        self.shift_start_dt = datetime.combine(today, start_time)
        self.shift_end_dt = datetime.combine(today, end_time)
        if self.shift_end_dt <= self.shift_start_dt:  # handle overnight shifts
            self.shift_end_dt += timedelta(days=1)

        self.tracker = ActivityTracker(self,idle_threshold=5)  # 10s idle threshold
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

        # Shift over
        if now > self.shift_end_dt and not self.shift_over:
            self.shift_over = True
            worked_minutes = self.shift_seconds // 60
            self.overtime_approved = ask_overtime(worked_minutes)
            if not self.overtime_approved:
                return

        # Overtime tracking
        if self.overtime_approved:
            self.shift_seconds += active + idle
            self.productive_seconds += active
            self.break_seconds += idle
            self.idle_seconds += idle
            self.overtime_seconds += active + idle

# ---------------- START APP ----------------
def start_attendance_app():
    attendance = AttendanceApp()
    ui = AttendifAIWidget(attendance)
    return ui


def main():
    initialize_db() 
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
