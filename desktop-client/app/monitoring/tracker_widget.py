from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont


class TrackerWindow(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.setWindowTitle("Activity Tracker")
        self.setFixedSize(360, 260)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e3c72,
                    stop:1 #2a5298
                );
            }
        """)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(14)

        title_font = QFont("Segoe UI", 10)
        value_font = QFont("Segoe UI", 18, QFont.Weight.Bold)

        self.shift_lbl = QLabel()
        self.shift_lbl.setFont(title_font)
        self.shift_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.shift_lbl.setStyleSheet("color: #555;")

        self.total_lbl = QLabel("00:00")
        self.total_lbl.setFont(value_font)
        self.total_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        total_title = QLabel("Total Shift Time")
        total_title.setFont(title_font)
        total_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.active_lbl = QLabel("00:00")
        self.active_lbl.setFont(value_font)
        self.active_lbl.setStyleSheet("color: #2ecc71;")

        active_title = QLabel("Productive")
        active_title.setFont(title_font)

        self.break_lbl = QLabel("00:00")
        self.break_lbl.setFont(value_font)
        self.break_lbl.setStyleSheet("color: #f39c12;")

        break_title = QLabel("Break")
        break_title.setFont(title_font)

        row = QHBoxLayout()
        row.addLayout(self.column(active_title, self.active_lbl))
        row.addLayout(self.column(break_title, self.break_lbl))

        card_layout.addWidget(self.shift_lbl)
        card_layout.addWidget(total_title)
        card_layout.addWidget(self.total_lbl)
        card_layout.addLayout(row)

        root = QVBoxLayout(self)
        root.addStretch()
        root.addWidget(card)
        root.addStretch()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000)

    def column(self, title, value):
        box = QVBoxLayout()
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box.addWidget(title)
        box.addWidget(value)
        return box

    def update_ui(self):
        self.shift_lbl.setText(
            f"Shift: {self.app.shift_start} - {self.app.shift_end}"
        )
        self.total_lbl.setText(self.format_time(self.app.shift_seconds))
        self.active_lbl.setText(self.format_time(self.app.productive_seconds))
        self.break_lbl.setText(self.format_time(self.app.break_seconds))

    @staticmethod
    def format_time(seconds):
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"
