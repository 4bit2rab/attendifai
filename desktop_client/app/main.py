
import sys
import getpass
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from datetime import datetime

class AttenFAIApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ATTENFAI Desktop Client")
        self.setGeometry(100, 100, 400, 200)

        self.user_label = QLabel(f"System User: {getpass.getuser()}")
        self.time_label = QLabel("Not Logged In")

        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(self.user_label)
        layout.addWidget(self.time_label)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

    def login(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText(f"Logged in at {now}")
        print(f"[ATTENFAI] Login recorded at {now}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AttenFAIApp()
    window.show()
    sys.exit(app.exec())
