import sys
import requests
from datetime import datetime, date
from PyQt5.QtWidgets import (QApplication, QMessageBox, QLabel, QVBoxLayout, QWidget)
from PyQt5.QtCore import QTimer

from tracker import ActivityTracker
from tracker_widget import TrackerWindow


# ---------------- FETCH SHIFT FROM API ----------------
def fetch_shift(employee_id):
    #http://127.0.0.1:9000/shift/{employee_id}-this endpoint created in the backend and works in the port 9000
    resp = requests.get(f"http://127.0.0.1:9000/shift/{employee_id}")
    resp.raise_for_status()
    data = resp.json()

    start = datetime.strptime(data["shift_start"], "%H:%M:%S").time()
    end = datetime.strptime(data["shift_end"], "%H:%M:%S").time()
    return start, end


# ---------------- OVERTIME POPUP ----------------
def ask_overtime(worked_minutes):
    app = QApplication.instance()
    if not app:
        raise RuntimeError("QApplication not running")

    msg = QMessageBox()
    msg.setWindowTitle("Overtime Detected")

    container = QWidget()
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

    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    start_time = datetime.now()

    timer = QTimer()

    def update_timer():
        elapsed = int((datetime.now() - start_time).total_seconds())
        m, s = divmod(elapsed, 60)
        timer_label.setText(f"{m:02d}:{s:02d}")

    timer.timeout.connect(update_timer)
    timer.start(1000)

    result = msg.exec_()
    timer.stop()

    return result == QMessageBox.Yes


# ---------------- MAIN ATTENDANCE LOGIC ----------------
class AttendanceApp:
    def __init__(self, employee_id):
        self.employee_id = employee_id

        start_time, end_time = fetch_shift(employee_id)
        today = date.today()

        # 🔑 USE DATETIME (not time)
        self.shift_start_dt = datetime.combine(today, start_time)
        self.shift_end_dt = datetime.combine(today, end_time)

        self.tracker = ActivityTracker(idle_threshold=10)
        self.tracker.start()

        self.shift_start = start_time.strftime("%H:%M")
        self.shift_end = end_time.strftime("%H:%M")

        self.shift_seconds = 0
        self.productive_seconds = 0
        self.break_seconds = 0

        self.shift_over = False
        self.overtime_approved = False

    def tick(self):
        now = datetime.now()

        # ---------------- BEFORE SHIFT ----------------
        if now < self.shift_start_dt:
            self.tracker.reset()
            return

        # ---------------- DURING SHIFT ----------------
        if self.shift_start_dt <= now <= self.shift_end_dt:
            self.tracker.tick()

            self.shift_seconds += 1
            self.productive_seconds += self.tracker.active_seconds
            self.break_seconds += self.tracker.break_seconds

            self.tracker.reset()
            return

        # ---------------- AFTER SHIFT ----------------
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
    app = QApplication(sys.argv)

    attendance = AttendanceApp(employee_id="EMP001")
    window = TrackerWindow(attendance)
    window.show()

    timer = QTimer()
    timer.timeout.connect(attendance.tick)
    timer.start(1000)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
