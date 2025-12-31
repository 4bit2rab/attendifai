# tracker.py
import time
import threading
from pynput import keyboard, mouse
from datetime import datetime
from dbConfig import add_session

class ActivityTracker:
    def __init__(self, app,idle_threshold=30):
        self.app=app
        self.idle_threshold = idle_threshold  # seconds
        self.last_activity = time.time()
        self.active_seconds = 0
        self.idle_seconds = 0
        self.lock = threading.Lock()
        self.state = "idle"  # "productive" or "idle"
        self.state_start_time = datetime.now()
        self._running = False

    def _on_activity(self):
        """Called on any keyboard/mouse activity"""
        with self.lock:
            self.last_activity = time.time()

    def start(self):
        """Start keyboard/mouse listeners and DB tracking thread"""
        self._running = True
        # Start input listeners
        keyboard.Listener(on_press=lambda k: self._on_activity()).start()
        mouse.Listener(
            on_move=lambda x, y: self._on_activity(),
            on_click=lambda x, y, b, p: self._on_activity(),
            on_scroll=lambda x, y, dx, dy: self._on_activity()
        ).start()
        # Start background thread to track sessions in DB
        threading.Thread(target=self._track_time_thread, daemon=True).start()

    def tick(self):
        """Called by GUI QTimer every second to update counters for widget"""
        with self.lock:
            elapsed = time.time() - self.last_activity
            if elapsed <= self.idle_threshold:
                self.active_seconds += 1
            else:
                self.idle_seconds += 1


    def _track_time_thread(self):
        """Background thread: track state changes and store in DB"""
        while self._running:
            time.sleep(1)
            now = datetime.now()
            with self.lock:
                elapsed = time.time() - self.last_activity
                current_state = "productive" if elapsed <= self.idle_threshold else "idle"

                # If state changed, write session to DB
                if current_state != self.state:
                    overtime=0
                    if (self.app.shift_over and not self.app.overtime_approved) or (self.app.overtime_approved and current_state=="idle"):
                        continue

                    if self.app.overtime_approved:
                        overtime=1
                    add_session(self.state, self.state_start_time, now,overtime)
                    self.state = current_state
                    self.state_start_time = now

    def get_and_reset_counters(self):
        """Return counters and reset for AttendanceApp GUI"""
        with self.lock:
            active = self.active_seconds
            idle = self.idle_seconds
            self.active_seconds = 0
            self.idle_seconds = 0
            return active, idle
