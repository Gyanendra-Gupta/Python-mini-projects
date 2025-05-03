# Create a personal budget tracker that visualizes income, expenses, and savings----

# A personal budget tracker helps you keep track of your monthly income, expenses, and savings. For example, 
# if you earn $3,000 a month, spend $2,000 on bills and groceries, the tracker will show you $1,000 in savings.
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import os

app = Flask(__name__)
def save_to_csv(budget_data):
    """
    Saves budget data to a CSV file.
    """
    df = pd.DataFrame(list(budget_data.items()), columns=['Category', 'Amount'])
    df.to_csv('personal_budget.csv', index=False)
    print("\nBudget data saved to 'personal_budget.csv'.")
def visualize_budget_data(budget_data):
    """
    Creates visualizations for budget data (bar chart and pie chart).
    """
    categories = list(budget_data.keys())
    amounts = list(budget_data.values())
    plt.figure(figsize=(10, 6))
    plt.bar(categories, amounts, color='lightblue')
    plt.title("Personal Budget Tracker")
    plt.xlabel("Categories")
    plt.ylabel("Amount ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the bar chart as an image
    bar_chart_path = "static/bar_chart.png"
    plt.savefig(bar_chart_path)
    plt.close()

    # Pie Chart (for expenses only)
    expense_categories = categories[1:-1]
    expense_amounts = amounts[1:-1]
    
    plt.figure(figsize=(8, 8))
    plt.pie(expense_amounts, labels=expense_categories, autopct='%1.1f%%', startangle=140)
    plt.title("Expense Breakdown")
    plt.axis('equal')

    # Save the pie chart as an image
    pie_chart_path = "static/pie_chart.png"
    plt.savefig(pie_chart_path)
    plt.close()

    return bar_chart_path, pie_chart_path
@app.route('/')
def index():
    """
    Renders the budget tracker form.
    """
    return render_template('finance.html')
@app.route('/track_budget', methods=['POST'])
def track_budget():
    # Extract form data
    income = float(request.form['income'])
    rent = float(request.form['rent'])
    utilities = float(request.form['utilities'])
    groceries = float(request.form['groceries'])
    transport = float(request.form['transport'])
    entertainment = float(request.form['entertainment'])
    other_expenses = float(request.form['other_expenses'])
    # Compute total expenses and savings
    total_expenses = rent + utilities + groceries + transport + entertainment + other_expenses
    savings = income - total_expenses
    # Store data in a dictionary
    budget_data = {
        "Income": income,
        "Rent": rent,
        "Utilities": utilities,
        "Groceries": groceries,
        "Transport": transport,
        "Entertainment": entertainment,
        "Other Expenses": other_expenses,
        "Savings": savings
    }
    # Save budget data to CSV
    save_to_csv(budget_data)
    # Generate budget visualizations
    bar_chart, pie_chart = visualize_budget_data(budget_data)
    # Render the result page with budget data and charts
    return render_template('result.html', budget_data=budget_data, bar_chart=bar_chart, pie_chart=pie_chart)

if __name__ == "__main__":
    app.run(debug=True)
