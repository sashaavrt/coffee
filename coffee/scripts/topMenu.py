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

def topMenu(start_date, end_date):
    df = pd.read_csv(url)

    df['date'] = pd.to_datetime(df['date'], format='mixed')
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df = df[(df['date'] > start_date) & (df['date'] < end_date)]

    df['daily_sum'] = df.groupby('date')['sales'].transform('sum')
    df = df.drop(["Unnamed: 0", "time"], axis=1)
    df['id'] = range(1, len(df) + 1)

    df['month'] = df['date'].dt.month_name()
    product_revenue = df.groupby('product')['sales'].sum().reset_index()
    top10_products = product_revenue.sort_values('sales', ascending=False).head(10)

    plt.style.use('ggplot')
    plt.figure(figsize=(6, 4))
    sns.barplot(x='product', y='sales', hue='product', data=top10_products)
    plt.xticks(rotation=90)
    plt.title('Top 10 Popular Products by Revenue', fontsize=18)
    plt.xlabel('Продукты')
    plt.ylabel('Продажи')
    plt.tight_layout()

    buffer_graph = BytesIO()
    plt.savefig(buffer_graph, format='png')
    buffer_graph.seek(0)
    graph_data = base64.b64encode(buffer_graph.getvalue()).decode('utf-8')
    buffer_graph.close()
    plt.close()

    buffer_table = BytesIO()
    top10_products.to_csv(buffer_table, index=False)
    buffer_table.seek(0)
    table_data = base64.b64encode(buffer_table.getvalue()).decode('utf-8')
    buffer_table.close()

    return graph_data, table_data