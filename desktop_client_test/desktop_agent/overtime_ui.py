import sys
import time
from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer


def ask_overtime(start_minutes):
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

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

    start_time = time.time()

    def update_timer():
        elapsed = int(time.time() - start_time)
        m = elapsed // 60
        s = elapsed % 60
        timer_label.setText(f"{m:02d}:{s:02d}")

    timer = QTimer()
    timer.timeout.connect(update_timer)
    timer.start(1000)

    result = msg.exec_()
    timer.stop()

    return result == QMessageBox.Yes
