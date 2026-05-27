from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, Signal, QPropertyAnimation, Property, QPoint
from PySide6.QtGui import QPainter, QColor, QFont, QPolygon
 
 
class CapsuleWidget(QWidget):
    """
    Screen-anchored handle with INTERNAL reveal animation
 
    """
 
    activated = Signal()
 
    HEIGHT = 140
    WIDTH = 46           # Window never changes
    REVEAL_MAX = 18      # How much pulls out visually
 
    def __init__(self):
        super().__init__()
 
        self._reveal = 0
 
        self.setFixedSize(self.WIDTH, self.HEIGHT)
 
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.Tool |
            Qt.WindowStaysOnTopHint
        )
 
        self.setAttribute(Qt.WA_TranslucentBackground)
 
        screen = QApplication.primaryScreen().availableGeometry()
        self.move(
            screen.right() - self.width(),
            int(screen.height() * 0.4)
        )
 
        self.anim = QPropertyAnimation(self, b"reveal", self)
        self.anim.setDuration(180)
 
    # ─────────────────────────────
    # Hover animation (INTERNAL)
    # ─────────────────────────────
    def enterEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._reveal)
        self.anim.setEndValue(self.REVEAL_MAX)
        self.anim.start()
        event.accept()
 
    def leaveEvent(self, event):
        self.anim.stop()
        self.anim.setStartValue(self._reveal)
        self.anim.setEndValue(0)
        self.anim.start()
        event.accept()
 
    # ─────────────────────────────
    # Click
    # ─────────────────────────────
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.activated.emit()
        super().mouseReleaseEvent(event)
 
    # ─────────────────────────────
    # Reveal property
    # ─────────────────────────────
    def getReveal(self):
        return self._reveal
 
    def setReveal(self, value):
        self._reveal = value
        self.update()
 
    reveal = Property(int, getReveal, setReveal)
 
    # ─────────────────────────────
    # Paint
    # ─────────────────────────────
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
 
        h = self.height()
        w = self.width()
        r = self._reveal
 
        # Wedge shape grows inward
        shape = QPolygon([
            QPoint(w, 0),
            QPoint(w, h),
            QPoint(w - r - 6, h - 12),
            QPoint(w - r - 6, 12),
        ])
 
        # Background (lighter ocean blue)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("#9bdcff"))
        painter.drawPolygon(shape)
 
        # Text
        painter.save()
        painter.translate(w - r / 2, h / 2)
        painter.rotate(-90)
 
        painter.setFont(QFont("Segoe UI", 9, QFont.Bold))
 
        painter.setPen(QColor("#0369a1"))
        painter.drawText(-h // 2, -8, h, 16, Qt.AlignCenter, "Attendif")
 
        painter.setPen(QColor("#1e3a8a"))
        painter.drawText(-h // 2 + 36, -8, h, 16, Qt.AlignCenter, "AI")
 
        painter.restore()