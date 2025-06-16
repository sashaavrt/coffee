import os
import pandas as pd
import joblib
from django.conf import settings
from sklearn.preprocessing import LabelEncoder

def predict_d(start_date, end_date):
    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, "model_d_supply.pkl")
    csv_path = os.path.join(current_dir, "coffee_sales.csv")

    df = pd.read_csv(csv_path)
    model = joblib.load(model_path)

    unique_items = df[['product', 'category', 'detail', 'location']].drop_duplicates()
    products_original = unique_items['product'].tolist()

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    future_dates = pd.date_range(start=start_date, end=end_date, freq='D')

    grid = pd.DataFrame([(d, *row) for d in future_dates for row in unique_items.values],
                        columns=['date', 'product', 'category', 'detail', 'location'])

    grid['hour'] = 12
    grid['day_of_week'] = grid['date'].dt.dayofweek
    grid['week'] = grid['date'].dt.isocalendar().week.astype(int)
    grid['quarter'] = grid['date'].dt.quarter
    grid['is_weekend'] = grid['day_of_week'] >= 5

    product_labels = grid['product'].copy()

    le = LabelEncoder()
    for col in ['category', 'product', 'detail', 'location']:
        grid[col] = le.fit_transform(grid[col].astype(str))

    features = ['category', 'product', 'detail', 'location', 'hour', 'day_of_week', 'week', 'quarter', 'is_weekend']
    X_pred = grid[features]
    y_pred = model.predict(X_pred)

    grid['predicted_quantity'] = y_pred
    grid['original_product'] = product_labels  
    total_by_product = grid.groupby('original_product')['predicted_quantity'].sum().round().astype(int)

    summary_lines = [f"{prod} — {qty} ед." for prod, qty in total_by_product.items()]
    return {
        "summary_list": summary_lines
    }
