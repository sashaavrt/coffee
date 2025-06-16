import os
import pandas as pd
import joblib
from django.conf import settings
from sklearn.preprocessing import LabelEncoder

def classify_load(value):
    if value < 5:
        return "🟦 Минимальная"
    elif value < 10:
        return "🟩 Низкая"
    elif value < 20:
        return "🟨 Средняя"
    elif value < 35:
        return "🟧 Выше средней"
    else:
        return "🟥 Максимальная"

def predict_c(start_date, end_date):
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, "coffee_sales.csv")
    model_path = os.path.join(current_dir, "model_c_staff.pkl")

    df = pd.read_csv(csv_path)
    model = joblib.load(model_path)

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    future_dates = pd.date_range(start=start_date, end=end_date, freq='D')

    top_locations = df['location'].value_counts().index[:3].tolist()

    grid = pd.DataFrame([(d, loc) for d in future_dates for loc in top_locations], columns=['date', 'location'])
    grid['hour'] = 12
    grid['day_of_week'] = grid['date'].dt.dayofweek
    grid['week'] = grid['date'].dt.isocalendar().week.astype(int)
    grid['quarter'] = grid['date'].dt.quarter
    grid['is_weekend'] = grid['day_of_week'] >= 5

    le = LabelEncoder()
    grid['location'] = le.fit_transform(grid['location'].astype(str))

    features = ['location', 'hour', 'day_of_week', 'week', 'quarter', 'is_weekend']
    X_pred = grid[features]
    y_pred = model.predict(X_pred)

    grid['predicted_load'] = y_pred
    daily = grid.groupby('date')['predicted_load'].mean().reset_index()

    daily['level'] = daily['predicted_load'].apply(classify_load)

    labels = daily['date'].dt.strftime('%d.%m').tolist()
    values = daily['predicted_load'].round(1).tolist()
    final_level = classify_load(daily['predicted_load'].mean())

    return {
        "summary": f"Средняя загрузка персонала: {final_level}",
        "chart_data": {
            "labels": labels,
            "values": values
        }
    }
