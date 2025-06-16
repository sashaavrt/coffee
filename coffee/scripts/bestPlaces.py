import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
from io import StringIO
import seaborn as sns
from coffee.templates import *
import base64 
from io import BytesIO

url = '/Users/sasha/Desktop/dipdev/coffee/scripts/coffee_sales.csv'

def bestPlaces(start_date, end_date):
    df = pd.read_csv(url)

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    df['date'] = pd.to_datetime(df['date'], format='mixed')
    df = df[(df['date'] > start_date) & (df['date'] < end_date)]

    # Построение графика
    plt.figure(figsize=(6, 4))
    location_revenue = df.groupby('location')['sales'].sum().reset_index()
    plt.style.use('ggplot')
    sns.barplot(data=location_revenue, x='location', y='sales', hue='location', errorbar=None)
    plt.title('Sales by Location', fontsize=18)
    plt.xlabel('Место')
    plt.ylabel('Продажи')
    plt.tight_layout()

    # Сохраняем график
    buffer_graph = BytesIO()
    plt.savefig(buffer_graph, format='png')
    buffer_graph.seek(0)
    graph_data = base64.b64encode(buffer_graph.getvalue()).decode('utf-8')
    buffer_graph.close()
    plt.close()

    # Сохраняем таблицу
    buffer_table = BytesIO()
    location_revenue.to_csv(buffer_table, index=False)
    buffer_table.seek(0)
    table_data = base64.b64encode(buffer_table.getvalue()).decode('utf-8')
    buffer_table.close()

    return graph_data, table_data

