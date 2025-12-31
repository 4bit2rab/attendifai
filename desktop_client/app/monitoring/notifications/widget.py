from PySide6.QtCore import QObject, QPropertyAnimation, QRect,QTimer
from PySide6.QtWidgets import QApplication
from ui.capsule import CapsuleWidget
from ui.sidebar import SideBarWidget

class AttendifAIWidget(QObject):
    """
    UI Controller
    Coordinates capsule + sidebar
    """
 
    def __init__(self,app):
        super().__init__()
        
        self.app=app
        self.logic_timer = QTimer(self)
        self.logic_timer.timeout.connect(self.app.tick)
        self.logic_timer.start(1000)

      
        self.ui_timer = QTimer(self)
        self.ui_timer.timeout.connect(self.update_ui)
        self.ui_timer.start(1000)

        # Handle
        self.capsule = CapsuleWidget()
        self.capsule.show()
 
        # Sidebar (START HIDDEN)
        self.sidebar = SideBarWidget(app)
        self.sidebar.hide()
 
        # self.app_state = AppState
 
        # Signals
        self.capsule.activated.connect(self.toggle_sidebar)
        self.sidebar.collapse_btn.clicked.connect(self.collapse_all)
 
        # 🔹 NEW: pre-attach sidebar to screen edge
        # self._attach_sidebar_to_edge()
 
        print("✅ AttendifAI UI controller initialized")
    
    def update_ui(self):
        self.sidebar.update_stats(
            self.format_time(self.app.productive_seconds),
            self.format_time(self.app.idle_seconds),
            self.format_time(self.app.productive_seconds+self.app.idle_seconds)
        )

    @staticmethod
    def format_time(seconds):
        m, s = divmod(int(seconds), 60)
        return f"{m:02d}:{s:02d}"
    
    # ---------------------------------
    # Sidebar control
    # ---------------------------------
 
    def toggle_sidebar(self):
        if self.sidebar.isVisible():
            self.collapse_all()
        else:
            self.show_sidebar()
            self.sidebar.start_auto_fade()
 
    def collapse_all(self):
        self.sidebar.hide()
 
 
    def show_sidebar(self):
        """
        Slide sidebar out from the handle
        """
        screen = QApplication.primaryScreen().availableGeometry()
 
        sidebar_height = int(screen.height() * 0.9)
        self.sidebar.setFixedHeight(sidebar_height)
 
        cap_geo = self.capsule.geometry()
        overlap = 8  # visual glue
 
        start_rect, end_rect = self._calculate_sidebar_geometry(
            cap_geo, sidebar_height, overlap
        )
 
        self._prepare_sidebar(start_rect)
        self._animate_sidebar(start_rect, end_rect)
 
        self._recenter_capsule(cap_geo, end_rect, sidebar_height)
 
    def _calculate_sidebar_geometry(self, cap_geo, sidebar_height, overlap):
        end_x = cap_geo.left() - self.sidebar.width() + overlap
        end_y = cap_geo.center().y() - sidebar_height // 2
 
        start_x = cap_geo.left() - overlap
        start_y = end_y
 
        start_rect = QRect(
            start_x,
            start_y,
            self.sidebar.width(),
            sidebar_height
        )
 
        end_rect = QRect(
            end_x,
            end_y,
            self.sidebar.width(),
            sidebar_height
        )
 
        return start_rect, end_rect
   
    def _prepare_sidebar(self, start_rect):
        self.sidebar.setGeometry(start_rect)
        self.sidebar.show()
 
    def _animate_sidebar(self, start_rect, end_rect):
        anim = QPropertyAnimation(self.sidebar, b"geometry")
        anim.setDuration(280)
        anim.setStartValue(start_rect)
        anim.setEndValue(end_rect)
        anim.start()
 
        self._sidebar_anim = anim  # keep alive
 
    def _recenter_capsule(self, cap_geo, end_rect, sidebar_height):
        self.capsule.move(
            cap_geo.x(),
            end_rect.y() + sidebar_height // 2 - self.capsule.height() // 2
        )
        self.capsule.raise_()