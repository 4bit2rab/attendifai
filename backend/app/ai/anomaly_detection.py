import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(report):
    anomalies = []

    for emp in report:
        if len(emp["logs"]) < 5:
            continue  # Not enough data

        df = pd.DataFrame(emp["logs"])
        df["productive_hours"] = df["productive_time"] / 3600

        model = IsolationForest(contamination=0.2, random_state=42)
        df["anomaly"] = model.fit_predict(df[["productive_hours"]])

        if -1 in df["anomaly"].values:
            anomalies.append({
                "employee_id": emp["employee_id"],
                "employee_name": emp["employee_name"],
                "reason": "Unusual productivity pattern detected"
            })

    return anomalies
