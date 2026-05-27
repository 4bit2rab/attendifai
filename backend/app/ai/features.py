import pandas as pd

def extract_employee_features(employee):
    logs = employee.get("logs", [])

    if not logs:
        return None

    df = pd.DataFrame(logs)

    df["productive_hours"] = df["productive_time"] / 3600
    df["idle_hours"] = df["idle_time"] / 3600
    df["overtime_hours"] = df["over_time"] / 3600

    return {
        "employee_id": employee["employee_id"],
        "employee_name": employee["employee_name"],
        "avg_productive_hours": df["productive_hours"].mean(),
        "avg_idle_hours": df["idle_hours"].mean(),
        "avg_overtime_hours": df["overtime_hours"].mean(),
        "working_days": len(df)
    }
