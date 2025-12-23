from pynput import keyboard, mouse
import time
import threading


class ActivityTracker:
    def __init__(self, idle_threshold=10):
        self.idle_threshold = idle_threshold
        self.last_activity = time.time()

        self.active_seconds = 0
        self.break_seconds = 0

        self.lock = threading.Lock()

    def _on_activity(self):
        with self.lock:
            self.last_activity = time.time()

    def start(self):
        keyboard.Listener(on_press=lambda k: self._on_activity()).start()
        mouse.Listener(
            on_move=lambda x, y: self._on_activity(),
            on_click=lambda x, y, b, p: self._on_activity(),
            on_scroll=lambda x, y, dx, dy: self._on_activity()
        ).start()

    def tick(self):
        with self.lock:
            if time.time() - self.last_activity <= self.idle_threshold:
                self.active_seconds += 1
            else:
                self.break_seconds += 1

    def reset(self):
        self.active_seconds = 0
        self.break_seconds = 0
