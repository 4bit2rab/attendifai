from backend.app.ai.constants import EXPECTED_WORKING_DAYS

def predict_next_week_productivity(features):
    base = features["avg_productive_hours"] * EXPECTED_WORKING_DAYS
    base += features["avg_overtime_hours"] * 2
    base -= features["avg_idle_hours"]
    return round(max(base, 0), 2)
