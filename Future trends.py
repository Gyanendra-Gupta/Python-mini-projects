# This project analyzes and visualizes sales data to identify trends and predict future performance.Using data analytics and visualization tools, 
# it provides insights into sales growth, customer behavior, and seasonal patterns. Predictive modeling helps forecast future sales,
# enabling informed business decisions.


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
data={'Date':pd.date_range(start='2023-01-01',periods=24,freq='M'),'Sales':[1200,1500,1800,2000,2200,2500,2700,3000,3200,3500,3800,4000,4200,4500,4800,5000,5300,5500,5800,6000,6300,6500,6800,7000]}
df=pd.DataFrame(data)
df['3-month MA']=df['Sales'].rolling(window=3).mean()
fig1=go.Figure()
fig1.add_trace(go.Scatter(x=df['Date'],y=df['Sales'],mode='lines+markers',name='Sales'))
fig1.add_trace(go.Scatter(x=df['Date'],y=df['3-month MA'],mode='lines',name='3-Month Moving Avg',line=dict(dash='dash')))
fig1.update_layout(title='Sales Trend Over Time',xaxis_title='Date',yaxis_title='Sales Amount',template='plotly_dark')
fig1.show()
df['Month']=df['Date'].dt.month_name()
monthly_sales=df.groupby('Month')['Sales'].sum().reset_index()
fig2=px.bar(monthly_sales,x='Month',y='Sales',title='Sales by Month',template='plotly_dark')
fig2.show()
df['Growth Rate']=df['Sales'].pct_change()
avg_growth_rate=df['Growth Rate'].mean()
last_sales=df['Sales'].iloc[-1]
predicted_sales=last_sales*(1+avg_growth_rate)
print(f"Predicted Sales for Next Month: {predicted_sales:.2f}")
