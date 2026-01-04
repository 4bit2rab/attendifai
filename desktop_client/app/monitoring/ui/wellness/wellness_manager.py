from ui.wellness.wellness_state import WellnessState

class WellnessManager:
    def __init__(self):
        self.water = WellnessState("water", 120)     # 5 min
        self.stretch = WellnessState("stretch", 300) # 15 min
        self.eyes = WellnessState("eyes", 90)       # 3 min

        self._all = [self.water, self.stretch, self.eyes]

    def update(self, productive_sec: int):
        print(f"[WellnessManager] update | productive={productive_sec}")

        triggered = []

        for state in self._all:
            if state.should_trigger(productive_sec):
                print(f"[WellnessManager] TRIGGER → {state.name}")
                state.mark_triggered(productive_sec)
                triggered.append(state.name)

        return triggered
