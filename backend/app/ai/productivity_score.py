import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def calculate_productivity_score(report):
    """
    Input: output of generate_employee_productivity_report
    """
    df = pd.DataFrame([
        {
            "employee_id": emp["employee_id"],
            "employee_name": emp["employee_name"],
            "total_productive_hours": emp["total_productive_hours"]
        }
        for emp in report
    ])

    scaler = MinMaxScaler(feature_range=(0, 100))
    df["productivity_score"] = scaler.fit_transform(
        df[["total_productive_hours"]]
    )

    return df.to_dict(orient="records")
