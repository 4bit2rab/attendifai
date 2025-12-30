# overtime.py
from PyQt6.QtWidgets import QMessageBox, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
import time

def ask_overtime(worked_minutes):
    msg = QMessageBox()
    msg.setWindowTitle("Overtime Detected")

    container = QWidget(msg)
    layout = QVBoxLayout(container)
    info = QLabel(f"You worked {worked_minutes} minutes beyond your shift.\nDo you want to continue as overtime?")
    layout.addWidget(info)
    msg.layout().addWidget(container)

    msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    result = msg.exec()
    return result == QMessageBox.StandardButton.Yes
