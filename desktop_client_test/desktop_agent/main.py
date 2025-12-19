import sys
from datetime import datetime, time as dtime
from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer

from tracker import ActivityTracker
from tracker_widget import TrackerWindow

# ---- CONFIG ----
SHIFT_START = dtime(17, 2)
SHIFT_END = dtime(17, 3)


def ask_overtime(start_minutes):
    """Show a dialog if overtime is detected."""
    app = QApplication.instance()
    if not app:
        raise RuntimeError("QApplication instance not found")

    msg = QMessageBox()
    msg.setWindowTitle("Overtime Detected")

    container = QWidget()
    layout = QVBoxLayout(container)

    info = QLabel(
        f"You worked {start_minutes} minutes beyond your shift.\n"
        "Overtime is still running:"
    )

    timer_label = QLabel("00:00")
    timer_label.setStyleSheet("font-size:18px;font-weight:bold")

    layout.addWidget(info)
    layout.addWidget(timer_label)
    msg.layout().addWidget(container)

    msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

    start_time = datetime.now()

    # Timer to update overtime duration
    timer = QTimer()
    def update_timer():
        elapsed = (datetime.now() - start_time).seconds
        m, s = divmod(elapsed, 60)
        timer_label.setText(f"{m:02d}:{s:02d}")

    timer.timeout.connect(update_timer)
    timer.start(1000)

    result = msg.exec_()
    timer.stop()

    return result == QMessageBox.Yes, (datetime.now() - start_time).seconds


class AttendanceApp:
    def __init__(self):
        self.tracker = ActivityTracker(idle_threshold=10)
        self.tracker.start()

        self.shift_start = SHIFT_START.strftime("%H:%M")
        self.shift_end = SHIFT_END.strftime("%H:%M")

        self.shift_seconds = 0
        self.productive_seconds = 0
        self.break_seconds = 0

        self.shift_over = False
        self.overtime_seconds = 0
        self.add_overtime_to_productive = False

    def tick(self):
        now = datetime.now().time()

        # BEFORE SHIFT → IGNORE EVERYTHING
        if now < SHIFT_START:
            self.tracker.reset()
            return

        # DURING SHIFT
        if SHIFT_START <= now <= SHIFT_END:
            self.tracker.tick()
            self.shift_seconds += 1
            self.productive_seconds += self.tracker.active_seconds
            self.break_seconds += self.tracker.break_seconds
            self.tracker.reset()
            return

        # AFTER SHIFT → OVERTIME
        if now > SHIFT_END:
            if not self.shift_over:
                self.shift_over = True
                start_minutes = self.shift_seconds // 60
                user_clicked_yes, overtime_elapsed = ask_overtime(start_minutes)

                if user_clicked_yes:
                    self.add_overtime_to_productive = True
                    self.overtime_seconds = overtime_elapsed

            # If user agreed, keep adding overtime seconds every tick
            if self.add_overtime_to_productive:
                self.overtime_seconds += 1
                self.shift_seconds += 1
                self.productive_seconds += 1


def main():
    app = QApplication(sys.argv)

    attendance = AttendanceApp()
    window = TrackerWindow(attendance)
    window.show()

    # Timer to update attendance every second
    timer = QTimer()
    timer.timeout.connect(attendance.tick)
    timer.start(1000)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
