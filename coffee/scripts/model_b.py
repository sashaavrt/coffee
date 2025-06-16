import os
import pandas as pd
from prophet import Prophet
import joblib

current_dir = os.path.dirname(__file__)
csv_path = os.path.join(current_dir, "coffee_sales.csv")
df = pd.read_csv(csv_path)

df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

product_ts = df.groupby(['datetime', 'product'])['quantity'].sum().reset_index()

models = {}
forecast_horizon = 7 

for product in product_ts['product'].unique():
    df_prod = product_ts[product_ts['product'] == product][['datetime', 'quantity']].rename(
        columns={'datetime': 'ds', 'quantity': 'y'}
    )

    if len(df_prod) < 10:
        continue 

    model = Prophet(daily_seasonality=True, weekly_seasonality=True)
    model.fit(df_prod)

    future = model.make_future_dataframe(periods=forecast_horizon)
    forecast = model.predict(future)

    future_forecast = forecast[['ds', 'yhat']].tail(forecast_horizon)
    total_predicted = future_forecast['yhat'].sum()

    models[product] = total_predicted

top3 = sorted(models.items(), key=lambda x: x[1], reverse=True)[:3]

model_path = os.path.join(current_dir, "model_b_top3.pkl")
joblib.dump(top3, model_path)
