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

le = LabelEncoder()
df = pd.read_csv("coffee_sales.csv")
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

X1 = df_encoded[enhanced_features]
y1 = df_encoded['quantity']
X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.2, random_state=42)

model_boosted = make_pipeline(StandardScaler(), GradientBoostingRegressor(n_estimators=100, random_state=42))
model_boosted.fit(X1_train, y1_train)
y1_pred = model_boosted.predict(X1_test)
r2_boosted = mean_absolute_percentage_error(y1_test, y1_pred)

y2 = df_encoded['sales']
X2_train, X2_test, y2_train, y2_test = train_test_split(X1, y2, test_size=0.2, random_state=42)

model_supply = make_pipeline(StandardScaler(), GradientBoostingRegressor(n_estimators=100, random_state=42))
model_supply.fit(X2_train, y2_train)
y2_pred = model_supply.predict(X2_test)
r2_supply_boosted = mean_absolute_percentage_error(y2_test, y2_pred)


top_locations_raw = df['location'].value_counts().index[:3]
staff_df = df[df['location'].isin(top_locations_raw)].copy()

staff_df['datetime'] = pd.to_datetime(staff_df['date'].astype(str) + ' ' + staff_df['time'])
staff_df['week'] = staff_df['datetime'].dt.isocalendar().week
staff_df['quarter'] = staff_df['datetime'].dt.quarter
staff_df['is_weekend'] = staff_df['day_of_week'] >= 5
staff_df['hour_bin'] = pd.cut(staff_df['hour'], bins=[0, 6, 12, 18, 24], labels=["Night", "Morning", "Afternoon", "Evening"])

for col in categorical_cols:
    staff_df[col] = le.fit_transform(staff_df[col].astype(str))

staff_df['load'] = staff_df['quantity'] + staff_df['sales']
X3 = staff_df[enhanced_features]
y3 = staff_df['load']

X3_train, X3_test, y3_train, y3_test = train_test_split(X3, y3, test_size=0.2, random_state=42)

model_staff = make_pipeline(StandardScaler(), GradientBoostingRegressor(n_estimators=100, random_state=42))
model_staff.fit(X3_train, y3_train)
y3_pred = model_staff.predict(X3_test)
r2_staff_boosted = mean_absolute_percentage_error(y3_test, y3_pred)

trend_data = df_encoded.groupby('day_of_week')['quantity'].mean().reset_index()
X4 = trend_data[['day_of_week']]
y4 = trend_data['quantity']

model_trend = LinearRegression()
model_trend.fit(X4, y4)
y4_pred = model_trend.predict(X4)
r2_trend_boosted = mean_absolute_percentage_error(y4, y4_pred)

