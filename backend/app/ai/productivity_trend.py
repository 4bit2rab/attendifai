import pandas as pd
from sklearn.linear_model import LinearRegression

def analyze_productivity_trend(report):
    trends = []

    for emp in report:
        if len(emp["logs"]) < 7:
            continue

        df = pd.DataFrame(emp["logs"])
        df["day_index"] = range(len(df))
        df["productive_hours"] = df["productive_time"] / 3600

        X = df[["day_index"]]
        y = df["productive_hours"]

        model = LinearRegression()
        model.fit(X, y)

        slope = model.coef_[0]

        trend = "stable"
        if slope > 0.05:
            trend = "improving"
        elif slope < -0.05:
            trend = "declining"

        trends.append({
            "employee_id": emp["employee_id"],
            "employee_name": emp["employee_name"],
            "trend": trend
        })

    return trends
