import time
from tracker import ActivityTracker

tracker = ActivityTracker(idle_threshold=10)
tracker.start()

while True:
    time.sleep(1)
    tracker.tick()
    print("Active seconds:", tracker.active_seconds)
