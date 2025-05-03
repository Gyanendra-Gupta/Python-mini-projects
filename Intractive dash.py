# This code makes a simple dashboard to show customer purchase trends. It uses a dropdown to filter data by category 
# and displays two charts: one for sales over time and another for top-selling products. The charts update 
# automatically when a category is selected. 🚀


import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
data = {'Customer': ['A', 'B', 'C', 'A', 'D', 'E', 'B', 'C', 'D', 'E'],
        'Product': ['Laptop', 'Phone', 'Tablet', 'Phone', 'Laptop', 'Tablet', 'Laptop', 'Phone', 'Tablet', 'Laptop'],
        'Category': ['Electronics', 'Electronics', 'Electronics', 'Electronics', 'Electronics', 'Electronics', 'Electronics', 'Electronics', 'Electronics', 'Electronics'],
        'Purchase Amount': [800, 600, 300, 500, 900, 350, 1000, 450, 380, 750],
        'Date': pd.date_range(start='2024-01-01', periods=10, freq='D')}
df = pd.DataFrame(data)
app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([html.H1("Customer Purchase Dashboard", style={'textAlign': 'center'}),dcc.Dropdown(id='category-dropdown',options=[{'label': cat, 'value': cat} for cat in df['Category'].unique()],value='Electronics',clearable=False),dcc.Graph(id='sales-trend'),dcc.Graph(id='top-products')])
@app.callback([Output('sales-trend', 'figure'), Output('top-products', 'figure')],[Input('category-dropdown', 'value')])
def update_charts(selected_category):
    filtered_df = df[df['Category'] == selected_category]
    sales_fig = px.line(filtered_df, x='Date', y='Purchase Amount', title='Sales Trend Over Time')
    product_fig = px.bar(filtered_df.groupby('Product')['Purchase Amount'].sum().reset_index(),x='Product', y='Purchase Amount', title='Top Selling Products')
    return sales_fig, product_fig
if __name__ == '__main__':
    app.run(debug=True)
