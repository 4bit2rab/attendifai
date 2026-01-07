# from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect, QApplication, QFrame, QProgressBar
# from PySide6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve
# from PySide6.QtGui import QFont, QColor, QMouseEvent
# from PySide6.QtWidgets import QGraphicsOpacityEffect
 
 
# class SideBarWidget(QWidget):
#     def __init__(self,app):
#         super().__init__()
 
#         self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
#         self.setFixedWidth(280)
#         # self.setAttribute(Qt.WA_TranslucentBackground)
 
#         self.pinned = False
#         self._drag_offset = QPoint()
 
#         self.setAttribute(Qt.WA_StyledBackground, True)
#         self.setWindowOpacity(1.0)
 
 
#         # ===== Layout =====
#         root = QVBoxLayout(self)
#         root.setContentsMargins(12, 12, 12, 12)
#         root.setSpacing(10)
 
#         # ===== Header =====
#         header = QVBoxLayout()
#         title = QLabel()
#         title.setText(
#             '<span style="color:#c7d2fe;">Attendif</span>'
#             '<span style="color:#1e3a8a;">AI</span>'
#         )
#         title.setStyleSheet("""
#             font-size: 17px;
#             font-weight: 600;
#             letter-spacing: 0.4px;
#             color: #EEF2FF;
#             border-radius: 18px;
#             """)
#         title.setAlignment(Qt.AlignCenter)
#         title.setFont(QFont("Segoe UI", 18, QFont.Bold))
 
#         subtitle = QLabel("Your work buddy")
#         subtitle.setStyleSheet("color:#A0A6BD; font-size:11px;")
#         subtitle.setAlignment(Qt.AlignCenter)
 
#         header.addWidget(title)
#         header.addWidget(subtitle)
#         root.addLayout(header)
 
#         # ===== Sections (placeholders) =====
#         #shift
#         title_font = QFont("Segoe UI", 10)
#         self.shift_lbl = QLabel()
#         self.shift_lbl.setFont(title_font)
#         self.shift_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         # self.shift_lbl.setStyleSheet("color: #555;")
#         self.shift_lbl.setStyleSheet("font-size:20px;")
#         root.addWidget(self.shift_lbl)
#         self.shift_lbl.setText(
#             f"Shift: {app.shift_start_dt.strftime('%H:%M')} - {app.shift_end_dt.strftime('%H:%M')}"
#         )
#         # total time
#         value_font = QFont("Segoe UI", 18, QFont.Weight.Bold)
#         self.total_lbl = QLabel("00:00")
#         self.total_lbl.setFont(value_font)
#         self.total_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.total_lbl.setStyleSheet("font-size:18px;")
#         root.addWidget(self.total_lbl)
 
#         self.status = QLabel()
#         self.status.setStyleSheet("""padding-top:5px;
#                                    padding-bottom:6px;
#                                   font-size:14px;
#                                   font-weight:400;
#                                   letter-spacing: 0.4px;
#                                   """)
#         root.addWidget(self.status)
 
#         # Progress Section
#         self.progress_label = QLabel("Today's Focus Progress")
#         self.progress_label.setStyleSheet("color: #B6BDD6;")
 
#         self.progress_bar = QProgressBar()
#         self.progress_bar.setRange(0, 100)
#         self.progress_bar.setValue(65)  # placeholder
 
#         self.appreciation_label = QLabel("Great consistency! Keep going 💙")
#         self.appreciation_label.setAlignment(Qt.AlignCenter)
#         self.appreciation_label.setStyleSheet("""
#         font-size: 12px;
#         color: #8FB7FF;
#         padding-bottom:10px;
#         """)
 
#         root.addWidget(self.progress_label)
#         root.addWidget(self.progress_bar)
#         root.addWidget(self.appreciation_label)
 
#         # Wellness Section
#         self.wellness_label = QLabel("Wellness Reminders")
#         self.wellness_label.setStyleSheet("""
#         font-weight: 500;
#         color: #B6BDD6;
#         """)
 
#         root.addWidget(self.wellness_label)
 
#         self.water_break = QLabel("💧 Water Break")
#         self.stretch_reminder = QLabel("🧘 Stretch Reminder")
#         self.eye_blink = QLabel("👁 Eye Blink Exercise")
 
#         for lbl in [self.water_break, self.stretch_reminder, self.eye_blink]:
#             lbl.setStyleSheet("""
#             background-color: #262A36;
#             padding: 10px 14px;
#             border-radius: 12px;
#             color: #E8ECF5;
#             """)
#             root.addWidget(lbl)
 
#         root.addStretch()
 
#         self.greeting_label = QLabel("Have a productive day ahead 🌤")
#         self.greeting_label.setAlignment(Qt.AlignCenter)
#         self.greeting_label.setStyleSheet("""
#         font-size: 12px;
#         color: #9AA1B8;
#         padding-top: 6px;
#         """)
 
#         root.addWidget(self.greeting_label)
 
 
#         # ===== Collapse Button =====
#         self.collapse_btn = QPushButton(">", self)
#         self.collapse_btn.setFixedSize(26, 60)
#         self.collapse_btn.setCursor(Qt.PointingHandCursor)
#         self.collapse_btn.setStyleSheet("""
#             QPushButton {
#                 background:#1e293b;
#                 color:white;
#                 border-radius:12px;
#             }
#             QPushButton:hover {
#                 background:#334155;
#             }
#         """)
#         self.collapse_btn.move(-13, 20)
#         self.collapse_btn.raise_()
 
 
#         # ===== Pin Button =====
#         self.pin_btn = QPushButton("📌", self)
#         self.pin_btn.setFixedSize(26, 26)
#         self.pin_btn.setStyleSheet("""
#             QPushButton {
#                 background:transparent;
#                 font-size:14px;
#                 border:none;
#             }
#         """)
#         self.pin_btn.clicked.connect(self.toggle_pin)
 
#         # ===== Styling =====
#         self.setStyleSheet("""
#         QWidget {
#             background-color: #1E1E26;
#             border-radius: 18px;
#         }
 
#         QFrame#SidebarContainer {
#             background-color: transparent;
#         }
 
#         QLabel {
#             color: #E6E9F0;
#             font-size: 13px;
#         }
#         QProgressBar {
#             background-color: #2A2D3A;
#             border-radius: 6px;
#             height: 10px;
#         }
 
#         QProgressBar::chunk {
#             background-color: qlineargradient(
#                 x1:0, y1:0, x2:1, y2:0,
#                 stop:0 #4F8CFF,
#                 stop:1 #3B82F6
#             );
#             border-radius: 8px;
# }
                           
#         QPushButton {
#             background-color: rgba(255, 255, 255, 20);
#             border: none;
#             border-radius: 8px;
#             color: white;
#             padding: 6px 10px;
#         }
 
#         QPushButton:hover {
#             background-color: rgba(255, 255, 255, 40);
#         }
#         """)
 
 
#         shadow = QGraphicsDropShadowEffect(self)
#         shadow.setBlurRadius(30)
#         shadow.setOffset(0, 0)
#         shadow.setColor(QColor(0, 0, 0, 160))
#         self.setGraphicsEffect(shadow)
 
#         # ===== Auto fade timer =====
#         self.fade_timer = QTimer(self)
#         self.fade_timer.setSingleShot(True)
#         self.fade_timer.timeout.connect(self.fade_out)
 
#         # ===== Wellness animations =====
#         self._water_anim = self.start_wellness_animation(self.water_break, delay=0)
#         self._stretch_anim = self.start_wellness_animation(self.stretch_reminder, delay=600)
#         self._eye_anim = self.start_wellness_animation(self.eye_blink, delay=1200)
 
#     def update_stats(self, productive, idle,total):
#         self.status.setText(
#             f"🟢 Productive: {productive}\n🔴 Idle: {idle}"
#         )
#         self.total_lbl.setText(
#             f"Total time :{total}"
#         )
#     # ---------- Behavior ----------
   
#     def start_wellness_animation(self, widget, delay=0):
#         effect = QGraphicsOpacityEffect(widget)
#         widget.setGraphicsEffect(effect)
 
#         anim = QPropertyAnimation(effect, b"opacity", self)
#         anim.setDuration(1800)
#         anim.setStartValue(1.0)
#         anim.setEndValue(0.55)
#         anim.setEasingCurve(QEasingCurve.InOutSine)
#         anim.setLoopCount(-1)
 
#         if delay:
#             anim.setStartValue(delay)
 
#         anim.start()
#         return anim
 
#     def toggle_pin(self):
#         self.pinned = not self.pinned
#         self.pin_btn.setText("📍" if self.pinned else "📌")
 
#     def start_auto_fade(self):
#         if not self.pinned:
#             self.fade_timer.start(10000)
 
#     def fade_out(self):
#         if not self.pinned:
#             self.hide()
 
#     def resizeEvent(self, event):
#         # Left edge collapse button
#         self.collapse_btn.move(-13, self.height() // 2 - 30)
 
#         # Pin button top-right
#         self.pin_btn.move(self.width() - 34, 12)
   
 
#      # ---------------- Drag ----------------
 
#     def mousePressEvent(self, event: QMouseEvent):
#         if event.button() == Qt.LeftButton:
#             self._dragging = True
#             self._drag_offset = event.globalPosition().toPoint() - self.pos()
 
#     def mouseMoveEvent(self, event: QMouseEvent):
#         if self._dragging:
#             self.move(event.globalPosition().toPoint() - self._drag_offset)
 
#     def mouseReleaseEvent(self, event: QMouseEvent):
#         self._dragging = False
#         self.snap_to_edge()
 
#     # ---------------- Magnetic edges ----------------
#     def snap_to_edge(self):
#         screen = QApplication.primaryScreen().availableGeometry()
#         geo = self.geometry()
 
#         SNAP = 24
#         x, y = geo.x(), geo.y()
 
#         if abs(geo.left() - screen.left()) < SNAP:
#             x = screen.left()
#         elif abs(geo.right() - screen.right()) < SNAP:
#             x = screen.right() - geo.width()
 
#         if abs(geo.top() - screen.top()) < SNAP:
#             y = screen.top()
#         elif abs(geo.bottom() - screen.bottom()) < SNAP:
#             y = screen.bottom() - geo.height()
 
#         self.move(x, y)
 
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QGraphicsDropShadowEffect, QApplication, QFrame, QProgressBar
from PySide6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QFont, QColor, QMouseEvent
from PySide6.QtWidgets import QGraphicsOpacityEffect
# from app.app_state import app_state
# from app.notifications.wellness_card import WellnessCard
# from app.notifications.wellness_cycle_guard import wellness_guard
# from app.ui.capsule_registry import get_capsule_widget
from ui.capsule_registry import register_capsule
from ui.wellness.wellness_manager import WellnessManager
from ui.widgets.wellness_badge import WellnessBadge
from PySide6.QtGui import QGuiApplication
 
class SideBarWidget(QWidget):
    def __init__(self,app):
        super().__init__()
 
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setFixedWidth(280)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
 
        self.pinned = False
        self._drag_offset = QPoint()
 
        self.setAttribute(Qt.WA_StyledBackground, False)
        self.setWindowOpacity(1.0)
 
        # ===== Layout =====
        root = QVBoxLayout(self)
        root.setContentsMargins(8, 8, 8, 8)
 
        self.container = QFrame()
        self.container.setObjectName("SidebarContainer")
 
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(12, 12, 12, 12)
        container_layout.setSpacing(12)
 
        root.addWidget(self.container)
 
        root.setStretch(0, 1)
       
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
        container_layout.addLayout(header)
 
        # ===== Sections (placeholders) =====
 
         #shift
        title_font = QFont("Segoe UI", 10)
        self.shift_lbl = QLabel()
        self.shift_lbl.setFont(title_font)
        self.shift_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.shift_lbl.setStyleSheet("color: #555;")
        self.shift_lbl.setStyleSheet("font-size:20px;")
        container_layout.addWidget(self.shift_lbl)
        self.shift_lbl.setText(
            f"Shift: {app.shift_start_dt.strftime('%H:%M')} - {app.shift_end_dt.strftime('%H:%M')}"
        )
 
        # # --- State badge ---
        # self.state_badge = QLabel("ACTIVE")
        # self.state_badge.setAlignment(Qt.AlignCenter)
        # self.state_badge.setFixedHeight(22)
        # self.state_badge.setStyleSheet("""
        #     background-color: #14532d;
        #     color: #bbf7d0;
        #     font-size: 11px;
        #     font-weight: 600;
        #     border-radius: 11px;
        # """)
 
        # container_layout.addWidget(self.state_badge)
 
        self.status = QLabel("🟢 Productive: 00:00\n🔴 Idle: 00:00")
        self.status.setStyleSheet("""padding-top:5px;
                                   padding-bottom:2px;
                                  font-size:14px;
                                  font-weight:400;
                                  letter-spacing: 0.4px;
                                  line-height:2;
                                  """)
        container_layout.addWidget(self.status)
       
   
        # Progress Section
        self.progress_label = QLabel("Today's Focus Progress")
        self.progress_label.setStyleSheet("color: #B6BDD6; font-size:12px;")
 
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)  # placeholder
 
        self.appreciation_label = QLabel("Great consistency! Keep going buddy💙")
        self.appreciation_label.setAlignment(Qt.AlignCenter)
        self.appreciation_label.setStyleSheet("""
        font-size: 12px;
        color: #8FB7FF;
        padding-bottom:10px;
        """)
 
        container_layout.addWidget(self.progress_label)
        container_layout.addWidget(self.progress_bar)
        container_layout.addWidget(self.appreciation_label)
 
        # app_state.telemetry.connect(self.on_productivity_update)
 
        # ===== Daily Summary =====
        self.summary_title = QLabel("Daily Summary")
        self.summary_title.setStyleSheet("""
            font-weight: 600;
            font-size:12px;
            color: #B6BDD6;
        """)
 
        self.summary_card = QFrame()
        self.summary_card.setStyleSheet("""
            background-color: #262A36;
            border-radius: 14px;
        """)
 
        summary_layout = QVBoxLayout(self.summary_card)
        summary_layout.setContentsMargins(12, 10, 12, 10)
        summary_layout.setSpacing(6)
 
        self.summary_tracked = QLabel("⏱ Tracked: 00:00:00")
        self.summary_active = QLabel("🟢 Active: 00:00:00")
        self.summary_idle = QLabel("🔴 Idle: 00:00:00")
        self.summary_score = QLabel("🎯 Score: 0%")
 
        for lbl in [
            self.summary_tracked,
            self.summary_active,
            self.summary_idle,
            self.summary_score
        ]:
            lbl.setStyleSheet("font-size:12px; color:#E5E7EB;")
 
        summary_layout.addWidget(self.summary_tracked)
        summary_layout.addWidget(self.summary_active)
        summary_layout.addWidget(self.summary_idle)
        summary_layout.addWidget(self.summary_score)
 
        container_layout.addWidget(self.summary_title)
        container_layout.addWidget(self.summary_card)
 
        # Wellness Section
       # ===== Wellness Reminders (NEW SYSTEM) =====
 
        self.wellness_label = QLabel("Wellness Reminders")
        self.wellness_label.setStyleSheet("""
            font-weight: 600;
            font-size:12px;
            color: #B6BDD6;
        """)
        container_layout.addWidget(self.wellness_label)
 
        # Vertical stack for badges
        self.wellness_stack = QVBoxLayout()
        self.wellness_stack.setSpacing(10)
        container_layout.addLayout(self.wellness_stack)
 
        # Wellness manager (logic)
        print("[Sidebar] Initializing WellnessManager")
        self.wellness_manager = WellnessManager()
 
        # Badges
        self.water_badge = WellnessBadge("Water",self)
        self.stretch_badge = WellnessBadge("Stretch",self)
        self.eyes_badge = WellnessBadge("Eyes",self)
 
        print("[Sidebar] Wellness badges initialized")
 
        self.wellness_stack.addWidget(self.water_badge)
        self.wellness_stack.addWidget(self.stretch_badge)
        self.wellness_stack.addWidget(self.eyes_badge)
 
        container_layout.addStretch()
 
        self.wellness_animation = QLabel("")
        self.wellness_animation.setAlignment(Qt.AlignCenter)
        self.wellness_animation.setStyleSheet("""
            font-size: 42px;
            color: #7AE7C7;
        """)
        self.wellness_animation.setVisible(False)
 
        container_layout.addWidget(self.wellness_animation)
 
        # ===== Wellness emoji animation (simple) =====
        self._wellness_anim_timer = QTimer(self)
        self._wellness_anim_timer.timeout.connect(self._animate_wellness_frame)
 
        self._wellness_anim_frames = []
        self._wellness_anim_index = 0
        self._active_wellness_name = None
 
 
     
 
        self.greeting_label = QLabel("Have a productive day ahead 🌤")
        self.greeting_label.setAlignment(Qt.AlignCenter)
        self.greeting_label.setStyleSheet("""
        font-size: 12px;
        color: #9AA1B8;
        padding-top: 6px;
        """)
 
        container_layout.addWidget(self.greeting_label)
 
        # ===== Collapse Button =====
        self.collapse_btn = QPushButton(">", self)
        self.collapse_btn.setFixedSize(26, 60)
        self.collapse_btn.setCursor(Qt.PointingHandCursor)
        self.collapse_btn.setStyleSheet("""
            QPushButton {
                background: #0F172A;
                color: #E5E7EB;
                border-radius: 12px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #1E293B;
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
 
        QFrame#SidebarContainer {
            background-color: #1E1E26;
            border-radius: 18px;
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
                           
        """)
 
        shadow = QGraphicsDropShadowEffect(self.container)
        shadow.setBlurRadius(32)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.container.setGraphicsEffect(shadow)
 
        # ===== Auto fade timer =====
        self.fade_timer = QTimer(self)
        self.fade_timer.setSingleShot(True)
        self.fade_timer.timeout.connect(self.fade_out)
 
       
 
    def update_stats(self,productive,idle):
 
        if productive and idle == 0:
            pass
       
        total = productive + idle
        percent = round((productive / total) * 100,2)
 
        def fmt(sec):
            sec = int(sec)
            h = sec // 3600
            m = (sec % 3600) // 60
            s = sec % 60
            return f"{h:02}:{m:02}:{s:02}"
 
        self.summary_tracked.setText(f"⏱ Tracked: {fmt(total)}")
        self.summary_active.setText(f"🟢 Active: {fmt(productive)}")
        self.summary_idle.setText(f"🔴 Idle: {fmt(idle)}")
        self.summary_score.setText(f"🎯 Score: {percent}%")
 
        self.status.setText(
            # f"<span style='color:{color};'>● {state}</span><br>"
            f"🟢 Productive: {fmt(productive)}<br>"
            f"🔴 Idle: {fmt(idle)}"
        )
 
        # Progress bar
        total = productive + idle
        percent = int((productive / total) * 100) if total > 0 else 0
        self.progress_bar.setValue(percent)
 
        # Appreciation hint (soft)
        if percent >= 70:
            self.appreciation_label.setText("Excellent focus today 💙")
        elif percent >= 40:
            self.appreciation_label.setText("Good momentum — keep going")
        else:
            self.appreciation_label.setText("Let’s get back on track 💪")
 
        self._update_wellness(productive)
   
 
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
 
        capsule_rect = self.collapse_btn.geometry()
        global_rect = QRect(
            self.mapToGlobal(capsule_rect.topLeft()),
            capsule_rect.size()
        )
        register_capsule(global_rect)
   
 
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
 
 
    def _update_wellness(self, productive_sec: int):
        print(f"[Sidebar] _update_wellness | productive={productive_sec}")
 
        # --- intervals (seconds) ---
        EYES_INTERVAL = 60
        WATER_INTERVAL = 120
        STRETCH_INTERVAL = 300
 
        # --- update progress (0 → 100) ---
        eyes_progress = int((productive_sec % EYES_INTERVAL) / EYES_INTERVAL * 100)
        water_progress = int((productive_sec % WATER_INTERVAL) / WATER_INTERVAL * 100)
        stretch_progress = int((productive_sec % STRETCH_INTERVAL) / STRETCH_INTERVAL * 100)
 
        self.eyes_badge.set_progress(eyes_progress)
        self.water_badge.set_progress(water_progress)
        self.stretch_badge.set_progress(stretch_progress)
 
        print(
            f"[WellnessProgress] eyes={eyes_progress}% | "
            f"water={water_progress}% | stretch={stretch_progress}%"
        )
 
        # --- trigger logic (unchanged) ---
        triggered = self.wellness_manager.update(productive_sec)
        print(f"[WellnessManager] triggered={triggered}")
 
        if "water" in triggered:
            self.water_badge.start_blink()
 
        if "stretch" in triggered:
            self.stretch_badge.start_blink()
 
        if "eyes" in triggered:
            self.eyes_badge.start_blink()
 
 
    def show_sidebar(self):
        print("[Sidebar] show_sidebar()")
        self.position_on_right()
        self.show()
        self.raise_()          # bring above other windows
        self.activateWindow()  # give it focus
 
    def hide_sidebar(self):
        print("[Sidebar] hide_sidebar()")
        if not self.pinned:
            self.hide()
 
    def on_wellness_started(self, name: str):
        print(f"[Sidebar] Wellness STARTED → {name}")
        self.show_sidebar()
        self.show_wellness_animation(name)
 
    def on_wellness_finished(self, name: str):
        print(f"[Sidebar] Wellness FINISHED → {name}")
        self.hide_wellness_animation()
        self.hide_sidebar()
 
    def show_wellness_animation(self, name: str):
        print(f"[Sidebar] Show animation for {name}")
 
        animations = {
            "Eyes": ["👁", "─", "👁", "─"],
            "Water": ["💧", "🥤", "💧", "🥤"],
            "Stretch": ["🧍‍♂️", "🙆‍♂️", "🧍‍♂️", "🙆‍♂️"]
        }
 
        self._active_wellness_name = name
        self._wellness_anim_frames = animations.get(name, ["✨"])
        self._wellness_anim_index = 0
 
        self.wellness_animation.setVisible(True)
        self._wellness_anim_timer.start(400)
 
        print(f"[WellnessAnimation] started → {name}")
 
 
        self.wellness_animation.setText((self._wellness_anim_frames[0]))
        self.wellness_animation.setVisible(True)
 
    def hide_wellness_animation(self):
        print("[Sidebar] Hide wellness animation")
 
        self._wellness_anim_timer.stop()
        self._wellness_anim_frames = []
        self._wellness_anim_index = 0
        self._active_wellness_name = None
 
        self.wellness_animation.setVisible(False)
 
 
    def _animate_wellness_frame(self):
        if not self._wellness_anim_frames:
            return
 
        frame = self._wellness_anim_frames[self._wellness_anim_index]
        self.wellness_animation.setText(frame)
 
        print(f"[WellnessAnimation] frame → {frame}")
 
        self._wellness_anim_index = (
            self._wellness_anim_index + 1
        ) % len(self._wellness_anim_frames)
 
   
 
    def position_on_right(self):
        screen = QGuiApplication.primaryScreen()
        screen_rect = screen.availableGeometry()
 
        sidebar_width = self.width()
        sidebar_height = self.height()
 
        x = screen_rect.right() - sidebar_width
        y = screen_rect.top() + 60  # slight offset from top (adjust if you want)
        self._dragging = True
 
        print(f"[Sidebar] Positioning on right → x={x}, y={y}")
        self.move(x, y)
 
 