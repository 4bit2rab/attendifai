from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QTimer, Signal


class OvertimeNotification(QWidget):
    approved = Signal(bool)

    def __init__(self, auto_close_ms=0):
        super().__init__(None)  # No parent → floating

        self.setWindowFlags(
            Qt.WindowType.Tool |
            Qt.WindowType.FramelessWindowHint|
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setFixedSize(300, 150)

        # ---------- Styling ----------
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border-radius: 12px;
            }

            QLabel {
                color: #ffffff;
                font-size: 15px;
                font-weight: 500;
            }

            QPushButton {
                padding: 8px 14px;
                border-radius: 6px;
                font-size: 13px;
            }

            QPushButton#yesBtn {
                background-color: #4da3ff;
                color: white;
            }

            QPushButton#yesBtn:hover {
                background-color: #6bb5ff;
            }

            QPushButton#noBtn {
                background-color: #3a3a3a;
                color: #dddddd;
            }

            QPushButton#noBtn:hover {
                background-color: #4a4a4a;
            }
        """)

        # ---------- Layout ----------
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 18, 20, 18)

        label = QLabel("Continue working overtime?")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        yes_btn = QPushButton("Yes")
        yes_btn.setObjectName("yesBtn")

        no_btn = QPushButton("No")
        no_btn.setObjectName("noBtn")

        yes_btn.clicked.connect(lambda: self._respond(True))
        no_btn.clicked.connect(lambda: self._respond(False))

        btn_layout.addWidget(yes_btn)
        btn_layout.addWidget(no_btn)

        layout.addWidget(label)
        layout.addLayout(btn_layout)

        # Optional auto close
        if auto_close_ms > 0:
            QTimer.singleShot(auto_close_ms, self.close)

    def _respond(self, value: bool):
        self.approved.emit(value)
        self.close()
