import os
import pandas as pd
import joblib
from django.conf import settings
from datetime import datetime
from sklearn.preprocessing import LabelEncoder

model_path = os.path.join(settings.BASE_DIR, 'coffee', 'scripts', 'model_a_sales.pkl')
model = joblib.load(model_path)

def predict_a(start_date, end_date, location_filter=None):
    current_dir = os.path.dirname(__file__)
    csv_path = os.path.join(current_dir, "coffee_sales.csv")
    df = pd.read_csv(csv_path)

    if not start_date or not end_date:
        return {
            "summary": "Некорректные даты — прогноз невозможен.",
            "chart_data": {"labels": [], "values": []}
        }

   
    dates = pd.date_range(start=start_date, end=end_date)

    if not location_filter:
        location_filter = df['location'].unique().tolist()

    grid = pd.DataFrame([(d, loc) for d in dates for loc in location_filter], columns=['date', 'location'])

    grid['hour'] = 12
    grid['day_of_week'] = grid['date'].dt.dayofweek
    grid['week'] = grid['date'].dt.isocalendar().week.astype(int)
    grid['quarter'] = grid['date'].dt.quarter
    grid['is_weekend'] = grid['day_of_week'] >= 5

    le = LabelEncoder()
    grid['location_encoded'] = le.fit_transform(grid['location'].astype(str))
    location_map = dict(zip(grid['location_encoded'], grid['location']))

    grid['location'] = grid['location_encoded']

    features = ['location', 'hour', 'day_of_week', 'week', 'quarter', 'is_weekend']
    X_pred = grid[features]

    y_pred = model.predict(X_pred) * 1000  
    grid['predicted_sales'] = y_pred

    grouped = grid.groupby('location')['predicted_sales'].sum().sort_values(ascending=False)

    labels = [location_map[loc] for loc in grouped.index.tolist()]
    values = grouped.values.tolist()
    total = sum(values)

    return {
        "summary": f"Прогноз выручки с {start_date} по {end_date}: {int(total):,} ₽",
        "chart_data": {
            "labels": labels,
            "values": values
        }
    }
