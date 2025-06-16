# Повторно определим LabelEncoder для использования в улучшенной предобработке
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from prophet import Prophet
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_percentage_error
import os

le = LabelEncoder()
current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "coffee_sales.csv")
df = pd.read_csv(csv_path)

df['datetime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['time'])
df.sort_values('datetime', inplace=True)
df['week'] = df['datetime'].dt.isocalendar().week
df['quarter'] = df['datetime'].dt.quarter
df['day_of_week'] = df['datetime'].dt.day_of_week
df['is_weekend'] = df['day_of_week'] >= 5
df['hour_bin'] = pd.cut(df['hour'], bins=[0, 6, 12, 18, 24], labels=["Night", "Morning", "Afternoon", "Evening"])

categorical_cols = ['category', 'product', 'detail', 'location', 'month', 'weekday', 'time_of_day', 'hour_bin']
df_encoded = df.copy()
for col in categorical_cols:
    df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))

enhanced_features = ['category', 'product', 'detail', 'location', 'hour', 'day_of_week', 'week', 'quarter', 'is_weekend']

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib as plt

enhanced_features = ['location', 'hour', 'day_of_week', 'week', 'quarter', 'is_weekend']

y_sales = df_encoded['sales']  
X_sales = df_encoded[enhanced_features]

X_train, X_test, y_train, y_test = train_test_split(X_sales, y_sales, test_size=0.2, random_state=42)
model_sales = make_pipeline(StandardScaler(), GradientBoostingRegressor(n_estimators=100, random_state=42))
model_sales.fit(X_train, y_train)
y_pred = model_sales.predict(X_test)

from sklearn.metrics import mean_absolute_percentage_error
mape = mean_absolute_percentage_error(y_test, y_pred)

print("MAPE:", mape)

import joblib
model_path = os.path.join(os.path.dirname(__file__), "model_a_sales.pkl")
joblib.dump(model_sales, model_path)