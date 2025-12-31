from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect, QApplication, QFrame, QProgressBar
from PySide6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QColor, QMouseEvent
from PySide6.QtWidgets import QGraphicsOpacityEffect

 
class SideBarWidget(QWidget):
    def __init__(self,app):
        super().__init__()
 
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setFixedWidth(280)
        # self.setAttribute(Qt.WA_TranslucentBackground)
 
        self.pinned = False
        self._drag_offset = QPoint()
 
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowOpacity(1.0)
 
 
        # ===== Layout =====
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(10)
 
        # ===== Header =====
        header = QVBoxLayout()
        title = QLabel()
        title.setText(
            '<span style="color:#c7d2fe;">Attendif</span>'
            '<span style="color:#1e3a8a;">AI</span>'
        )
        title.setStyleSheet("""
            font-size: 17px;
            font-weight: 600;
            letter-spacing: 0.4px;
            color: #EEF2FF;
            border-radius: 18px;
            """)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
 
        subtitle = QLabel("Your work buddy")
        subtitle.setStyleSheet("color:#A0A6BD; font-size:11px;")
        subtitle.setAlignment(Qt.AlignCenter)
 
        header.addWidget(title)
        header.addWidget(subtitle)
        root.addLayout(header)
 
        # ===== Sections (placeholders) =====
        #shift
        title_font = QFont("Segoe UI", 10)
        self.shift_lbl = QLabel()
        self.shift_lbl.setFont(title_font)
        self.shift_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.shift_lbl.setStyleSheet("color: #555;")
        self.shift_lbl.setStyleSheet("font-size:20px;")
        root.addWidget(self.shift_lbl)
        self.shift_lbl.setText(
            f"Shift: {app.shift_start_dt.strftime('%H:%M')} - {app.shift_end_dt.strftime('%H:%M')}"
        )
        # total time
        value_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
        self.total_lbl = QLabel("00:00")
        self.total_lbl.setFont(value_font)
        self.total_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.total_lbl.setStyleSheet("font-size:18px;")
        root.addWidget(self.total_lbl)

        self.status = QLabel()
        self.status.setStyleSheet("""padding-top:5px;
                                   padding-bottom:6px;
                                  font-size:14px;
                                  font-weight:400;
                                  letter-spacing: 0.4px;
                                  """)
        root.addWidget(self.status)
 
        # Progress Section
        self.progress_label = QLabel("Today's Focus Progress")
        self.progress_label.setStyleSheet("color: #B6BDD6;")
 
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(65)  # placeholder
 
        self.appreciation_label = QLabel("Great consistency! Keep going 💙")
        self.appreciation_label.setAlignment(Qt.AlignCenter)
        self.appreciation_label.setStyleSheet("""
        font-size: 12px;
        color: #8FB7FF;
        padding-bottom:10px;
        """)
 
        root.addWidget(self.progress_label)
        root.addWidget(self.progress_bar)
        root.addWidget(self.appreciation_label)
 
        # Wellness Section
        self.wellness_label = QLabel("Wellness Reminders")
        self.wellness_label.setStyleSheet("""
        font-weight: 500;
        color: #B6BDD6;
        """)
 
        root.addWidget(self.wellness_label)
 
        self.water_break = QLabel("💧 Water Break")
        self.stretch_reminder = QLabel("🧘 Stretch Reminder")
        self.eye_blink = QLabel("👁 Eye Blink Exercise")
 
        for lbl in [self.water_break, self.stretch_reminder, self.eye_blink]:
            lbl.setStyleSheet("""
            background-color: #262A36;
            padding: 10px 14px;
            border-radius: 12px;
            color: #E8ECF5;
            """)
            root.addWidget(lbl)
 
        root.addStretch()
 
        self.greeting_label = QLabel("Have a productive day ahead 🌤")
        self.greeting_label.setAlignment(Qt.AlignCenter)
        self.greeting_label.setStyleSheet("""
        font-size: 12px;
        color: #9AA1B8;
        padding-top: 6px;
        """)
 
        root.addWidget(self.greeting_label)
 
 
        # ===== Collapse Button =====
        self.collapse_btn = QPushButton(">", self)
        self.collapse_btn.setFixedSize(26, 60)
        self.collapse_btn.setCursor(Qt.PointingHandCursor)
        self.collapse_btn.setStyleSheet("""
            QPushButton {
                background:#1e293b;
                color:white;
                border-radius:12px;
            }
            QPushButton:hover {
                background:#334155;
            }
        """)
        self.collapse_btn.move(-13, 20)
        self.collapse_btn.raise_()
 
 
        # ===== Pin Button =====
        self.pin_btn = QPushButton("📌", self)
        self.pin_btn.setFixedSize(26, 26)
        self.pin_btn.setStyleSheet("""
            QPushButton {
                background:transparent;
                font-size:14px;
                border:none;
            }
        """)
        self.pin_btn.clicked.connect(self.toggle_pin)
 
        # ===== Styling =====
        self.setStyleSheet("""
        QWidget {
            background-color: #1E1E26;
            border-radius: 18px;
        }
 
        QFrame#SidebarContainer {
            background-color: transparent;
        }
 
        QLabel {
            color: #E6E9F0;
            font-size: 13px;
        }
        QProgressBar {
            background-color: #2A2D3A;
            border-radius: 6px;
            height: 10px;
        }
 
        QProgressBar::chunk {
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #4F8CFF,
                stop:1 #3B82F6
            );
            border-radius: 8px;
}
                           
        QPushButton {
            background-color: rgba(255, 255, 255, 20);
            border: none;
            border-radius: 8px;
            color: white;
            padding: 6px 10px;
        }
 
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 40);
        }
        """)
 
 
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(shadow)
 
        # ===== Auto fade timer =====
        self.fade_timer = QTimer(self)
        self.fade_timer.setSingleShot(True)
        self.fade_timer.timeout.connect(self.fade_out)
 
        # ===== Wellness animations =====
        self._water_anim = self.start_wellness_animation(self.water_break, delay=0)
        self._stretch_anim = self.start_wellness_animation(self.stretch_reminder, delay=600)
        self._eye_anim = self.start_wellness_animation(self.eye_blink, delay=1200)

    def update_stats(self, productive, idle,total):
        self.status.setText(
            f"🟢 Productive: {productive}\n🔴 Idle: {idle}"
        ) 
        self.total_lbl.setText(
            f"Total time :{total}"
        ) 
    # ---------- Behavior ----------
    
    def start_wellness_animation(self, widget, delay=0):
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
 
        anim = QPropertyAnimation(effect, b"opacity", self)
        anim.setDuration(1800)
        anim.setStartValue(1.0)
        anim.setEndValue(0.55)
        anim.setEasingCurve(QEasingCurve.InOutSine)
        anim.setLoopCount(-1)
 
        if delay:
            anim.setStartValue(delay)
 
        anim.start()
        return anim
 
    def toggle_pin(self):
        self.pinned = not self.pinned
        self.pin_btn.setText("📍" if self.pinned else "📌")
 
    def start_auto_fade(self):
        if not self.pinned:
            self.fade_timer.start(10000)
 
    def fade_out(self):
        if not self.pinned:
            self.hide()
 
    def resizeEvent(self, event):
        # Left edge collapse button
        self.collapse_btn.move(-13, self.height() // 2 - 30)
 
        # Pin button top-right
        self.pin_btn.move(self.width() - 34, 12)
   
 
     # ---------------- Drag ----------------
 
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._dragging = True
            self._drag_offset = event.globalPosition().toPoint() - self.pos()
 
    def mouseMoveEvent(self, event: QMouseEvent):
        if self._dragging:
            self.move(event.globalPosition().toPoint() - self._drag_offset)
 
    def mouseReleaseEvent(self, event: QMouseEvent):
        self._dragging = False
        self.snap_to_edge()
 
    # ---------------- Magnetic edges ----------------
    def snap_to_edge(self):
        screen = QApplication.primaryScreen().availableGeometry()
        geo = self.geometry()
 
        SNAP = 24
        x, y = geo.x(), geo.y()
 
        if abs(geo.left() - screen.left()) < SNAP:
            x = screen.left()
        elif abs(geo.right() - screen.right()) < SNAP:
            x = screen.right() - geo.width()
 
        if abs(geo.top() - screen.top()) < SNAP:
            y = screen.top()
        elif abs(geo.bottom() - screen.bottom()) < SNAP:
            y = screen.bottom() - geo.height()
 
        self.move(x, y)