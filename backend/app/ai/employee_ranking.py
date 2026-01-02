import pandas as pd
from typing import List
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
from backend.app.models.models import EmployeeInput

def rank_employees_ai(employees: List[EmployeeInput]):
    # Convert input to DataFrame
    df = pd.DataFrame([{
        "employee_id": e.employee_id,
        "employee_name": e.employee_name,
        "productive_hours": e.total_productive_hours,
        "overtime_hours": e.total_overtime_hours,
        "log_count": len(e.logs)
    } for e in employees])

    if df.empty:
        return []

    # AI Features
    X = df[["productive_hours", "overtime_hours", "log_count"]]

    # Synthetic target for ranking
    y = df["productive_hours"]

    # Train AI model
    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )
    model.fit(X, y)

    # Predict scores
    df["ai_raw_score"] = model.predict(X)

    # Normalize scores to 0–100
    scaler = MinMaxScaler(feature_range=(0, 100))
    df["productivity_score"] = scaler.fit_transform(
        df[["ai_raw_score"]]
    )

    # Rank
    df = df.sort_values(
        by="productivity_score",
        ascending=False
    ).reset_index(drop=True)

    df["rank"] = df.index + 1

    # Performance labels
    def label(score):
        if score >= 80:
            return "Excellent"
        elif score >= 50:
            return "Good"
        elif score >= 30:
            return "Average"
        return "Poor"

    df["performance"] = df["productivity_score"].apply(label)

    return df[[
        "rank",
        "employee_id",
        "employee_name",
        "productivity_score",
        "performance"
    ]].to_dict(orient="records")
