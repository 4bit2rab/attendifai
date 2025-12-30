# tracker_widget.py
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

class TrackerWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Activity Tracker")
        self.setFixedSize(360, 260)
        self.setStyleSheet("QWidget {background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e3c72, stop:1 #2a5298);}")

        layout = QVBoxLayout()
        title_font = QFont("Segoe UI", 10)
        value_font = QFont("Segoe UI", 18, QFont.Weight.Bold)

        # Shift
        self.shift_lbl = QLabel()
        self.shift_lbl.setFont(title_font)
        self.shift_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.shift_lbl.setStyleSheet("color: #555;")
        layout.addWidget(self.shift_lbl)

        # Total
        layout.addWidget(QLabel("Total Time"))
        self.total_lbl = QLabel("00:00")
        self.total_lbl.setFont(value_font)
        self.total_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.total_lbl)

        # Productive
        layout.addWidget(QLabel("Productive"))
        self.active_lbl = QLabel("00:00")
        self.active_lbl.setFont(value_font)
        self.active_lbl.setStyleSheet("color: #2ecc71;")
        layout.addWidget(self.active_lbl)

        # Break
        layout.addWidget(QLabel("Break"))
        self.break_lbl = QLabel("00:00")
        self.break_lbl.setFont(value_font)
        self.break_lbl.setStyleSheet("color: #f39c12;")
        layout.addWidget(self.break_lbl)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000)

    def update_ui(self):
        self.shift_lbl.setText(
            f"Shift: {self.app.shift_start_dt.strftime('%H:%M')} - {self.app.shift_end_dt.strftime('%H:%M')}"
        )
        total_seconds = self.app.productive_seconds + self.app.idle_seconds + self.app.overtime_seconds
        self.total_lbl.setText(self.format_time(total_seconds))
        self.active_lbl.setText(self.format_time(self.app.productive_seconds))
        self.break_lbl.setText(self.format_time(self.app.idle_seconds))

    @staticmethod
    def format_time(seconds):
        m, s = divmod(int(seconds), 60)
        return f"{m:02d}:{s:02d}"
