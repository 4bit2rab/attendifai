from PySide6.QtWidgets import QLabel
from PySide6.QtCore import QTimer
 
 
class WellnessBadge(QLabel):
    BLINK_INTERVAL_MS = 500
    BLINK_DURATION_MS = 10000  # 10 seconds
 
    def __init__(self, title: str, sidebar):
        super().__init__(title)
 
        self.title = title
        self.sidebar = sidebar
 
        self.progress = 0  # 0 → 100
        self._blink_on = False
        self._is_blinking = False
 
        self._blink_timer = QTimer(self)
        self._blink_timer.timeout.connect(self._toggle_blink)
 
        self._stop_timer = QTimer(self)
        self._stop_timer.setSingleShot(True)
        self._stop_timer.timeout.connect(self.stop_blink)
 
        self._apply_progress_style()
 
    # ───────────── PUBLIC API ─────────────
 
    def set_progress(self, percent: int):
        if self._is_blinking:
            return  # don't override blink visuals
 
        self.progress = max(0, min(100, percent))
        print(f"[WellnessBadge] {self.title} progress → {self.progress}%")
        self._apply_progress_style()
 
    def start_blink(self):
        if self._is_blinking:
            return
 
        print(f"[WellnessBadge] start blink → {self.title}")
 
        self._is_blinking = True
        self.sidebar.on_wellness_started(self.title)
 
        self._blink_timer.start(self.BLINK_INTERVAL_MS)
        self._stop_timer.start(self.BLINK_DURATION_MS)
 
    def stop_blink(self):
        print(f"[WellnessBadge] stop blink → {self.title}")
 
        self._blink_timer.stop()
        self._is_blinking = False
        self.progress = 0
 
        self._apply_progress_style()
        self.sidebar.on_wellness_finished(self.title)
 
    # ───────────── INTERNAL ─────────────
 
    def _toggle_blink(self):
        if self._blink_on:
            self._apply_blink_off_style()
        else:
            self._apply_blink_on_style()
 
        self._blink_on = not self._blink_on
 
    # ───────────── STYLES ─────────────
 
    def _apply_progress_style(self):
        self.setStyleSheet(f"""
            QLabel {{
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3B82F6,
                    stop:{self.progress / 100:.2f} #3B82F6,
                    stop:{self.progress / 100:.2f} #262A36,
                    stop:1 #262A36
                );
                padding: 10px 14px;
                border-radius: 12px;
                color: #E8ECF5;
            }}
        """)
 
    def _apply_blink_on_style(self):
        self.setStyleSheet("""
            background-color: #3B82F6;
            padding: 10px 14px;
            border-radius: 12px;
            color: white;
        """)
 
    def _apply_blink_off_style(self):
        self.setStyleSheet("""
            background-color: #262A36;
            padding: 10px 14px;
            border-radius: 12px;
            color: #E8ECF5;
        """)
 
 
 