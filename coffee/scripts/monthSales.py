import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
from io import StringIO
import seaborn as sns
from io import BytesIO
import base64

url = '/Users/sasha/Desktop/dipdev/coffee/scripts/coffee_sales.csv'

def monthSales(start_date, end_date):
    df = pd.read_csv(url)

    df['date'] = pd.to_datetime(df['date'], format='mixed')
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df = df[(df['date'] > start_date) & (df['date'] < end_date)]

    df['daily_sum'] = df.groupby('date')['sales'].transform('sum')
    df = df.drop(["Unnamed: 0", "time"], axis=1)
    df['id'] = range(1, len(df) + 1)

    df['month'] = df['date'].dt.month_name()
    revenue = df.groupby('month')['sales'].sum().reset_index()

    plt.figure(figsize=(6, 4))
    month_order = ['January', 'February', 'March', 'April', 'May', 'June']
    plt.style.use('ggplot')
    sns.barplot(data=revenue, x='month', y='sales', hue='month', order=month_order, errorbar=None)
    plt.title('Sales by Month', fontsize=18)
    plt.xlabel('Месяц')
    plt.ylabel('Продажи')
    plt.tight_layout()

    buffer_graph = BytesIO()
    plt.savefig(buffer_graph, format='png')
    buffer_graph.seek(0)
    graph_data = base64.b64encode(buffer_graph.getvalue()).decode('utf-8')
    buffer_graph.close()
    plt.close()

    buffer_table = BytesIO()
    revenue.to_csv(buffer_table, index=False)
    buffer_table.seek(0)
    table_data = base64.b64encode(buffer_table.getvalue()).decode('utf-8')
    buffer_table.close()

    return graph_data, table_data