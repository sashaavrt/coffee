import os
import pandas as pd
import joblib
import numpy as np

def predict_b(start_date, end_date):
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, "model_b_top3.pkl")

    top3 = joblib.load(model_path) 

    top3_names = [name for name, _ in top3]
    summary_list = [f"{i+1}. {name}" for i, name in enumerate(top3_names)]

    num_days = 15
    dates = pd.date_range(start=pd.to_datetime(start_date), periods=num_days).strftime('%d.%m').tolist()

    chart_data = {
        "labels": dates,
        "datasets": []
    }

    for i, name in enumerate(top3_names):
        base = 10 + i * 5
        trend = (np.sin(np.linspace(0, np.pi, num_days)) * 5 + base).round(2).tolist()
        chart_data["datasets"].append({
            "label": name,
            "data": trend,
            "fill": True
        })

    return {
        "summary_list": summary_list,
        "chart_data": chart_data
    }
