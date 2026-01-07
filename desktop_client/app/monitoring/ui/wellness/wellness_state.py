class WellnessState:
    def __init__(self, name: str, interval_sec: int):
        self.name = name
        self.interval = interval_sec
        self.last_trigger_at = 0
        self.is_blinking = False
 
    def should_trigger(self, productive_sec: int) -> bool:
        return productive_sec - self.last_trigger_at >= self.interval
 
    def mark_triggered(self, productive_sec: int):
        self.last_trigger_at = productive_sec
        self.is_blinking = True
 
    def stop(self):
        self.is_blinking = False
 
 