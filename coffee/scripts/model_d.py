import os
import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder

current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "coffee_sales.csv")
df = pd.read_csv(csv_path)

df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
df.sort_values('datetime', inplace=True)
df['week'] = df['datetime'].dt.isocalendar().week.astype(int)
df['quarter'] = df['datetime'].dt.quarter
df['day_of_week'] = df['datetime'].dt.dayofweek
df['is_weekend'] = df['day_of_week'] >= 5

categorical_cols = ['category', 'product', 'detail', 'location']
for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))

features = ['category', 'product', 'detail', 'location', 'hour', 'day_of_week', 'week', 'quarter', 'is_weekend']
df = df.dropna(subset=features + ['quantity'])

X = df[features]
y = df['quantity']

model = make_pipeline(StandardScaler(), GradientBoostingRegressor(n_estimators=100, random_state=42))
model.fit(X, y)

model_path = os.path.join(current_dir, "model_d_supply.pkl")
joblib.dump(model, model_path)
