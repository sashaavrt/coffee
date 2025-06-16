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
df['day_of_week'] = df['datetime'].dt.dayofweek
df['week'] = df['datetime'].dt.isocalendar().week.astype(int)
df['quarter'] = df['datetime'].dt.quarter
df['is_weekend'] = df['day_of_week'] >= 5

top_locations = df['location'].value_counts().index[:3]
df = df[df['location'].isin(top_locations)].copy()

df['load'] = df['quantity'] + df['sales']

le = LabelEncoder()
df['location'] = le.fit_transform(df['location'].astype(str))
features = ['location', 'hour', 'day_of_week', 'week', 'quarter', 'is_weekend']

df = df.dropna(subset=features + ['load'])

X = df[features]
y = df['load']

pipeline = make_pipeline(StandardScaler(), GradientBoostingRegressor(n_estimators=100, random_state=42))
pipeline.fit(X, y)

model_path = os.path.join(current_dir, "model_c_staff.pkl")
joblib.dump(pipeline, model_path)
