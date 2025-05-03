# This program tracks and visualizes fitness activities , such as running, cycling, or gym  workouts,
# by logging details like duration, calories burned, and distance covered.It then generates barplots
# to show how these activities change over time, helping users easily track their progress.


import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# 1. Set up the SQLite database to store fitness activities
def create_database():
    conn = sqlite3.connect("fitness_tracker.db")
    c = conn.cursor()
    
    # Create a table for fitness activities if it doesn't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_type TEXT,
        duration_minutes INTEGER,
        calories_burned INTEGER,
        distance_km REAL,
        activity_date TEXT
    )
    ''')
    conn.commit()
    conn.close()

# 2. Function to log fitness activity data (user input)
def log_activity():
    conn = sqlite3.connect("fitness_tracker.db")
    c = conn.cursor()

    # Take user input for activity details
    activity_type = input("Enter the type of activity (e.g., Running, Cycling, Gym): ")
    duration_minutes = int(input("Enter the duration of the activity in minutes: "))
    calories_burned = int(input("Enter the number of calories burned: "))
    distance_km = float(input("Enter the distance covered in kilometers: "))
    activity_date = input("Enter the activity date (YYYY-MM-DD): ")

    # Insert the activity data into the table
    c.execute('''
    INSERT INTO activities (activity_type, duration_minutes, calories_burned, distance_km, activity_date)
    VALUES (?, ?, ?, ?, ?)
    ''', (activity_type, duration_minutes, calories_burned, distance_km, activity_date))
    
    conn.commit()
    conn.close()
    print("Activity logged successfully.")

# 3. Function to fetch all activities from the database and return them as a Pandas DataFrame
def fetch_activities():
    conn = sqlite3.connect("fitness_tracker.db")
    df = pd.read_sql_query("SELECT * FROM activities", conn)
    conn.close()
    return df

# 4. Function to visualize fitness progress over time with bar plots
def visualize_progress():
    # Fetch the data from the database
    df = fetch_activities()
    
    # Check if data exists
    if df.empty:
        print("No activity data found.")
        return
    
    # Convert activity_date to datetime for better plotting
    df['activity_date'] = pd.to_datetime(df['activity_date'], errors='coerce')
    
    # Set Seaborn style for attractive visualization
    sns.set(style="whitegrid")

    # Bar plot for calories burned over time
    plt.figure(figsize=(12, 6))
    bar_plot = sns.barplot(x='activity_date', y='calories_burned', data=df, palette='Blues_d')
    plt.title('Calories Burned Over Time', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Calories Burned', fontsize=12)
    plt.xticks(rotation=45)
    
    # Annotate the bars with the exact value
    for p in bar_plot.patches:
        bar_plot.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                          ha='center', va='center', fontsize=10, color='black', xytext=(0, 8), 
                          textcoords='offset points')
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # Bar plot for distance covered over time
    plt.figure(figsize=(12, 6))
    bar_plot = sns.barplot(x='activity_date', y='distance_km', data=df, palette='Greens_d')
    plt.title('Distance Covered Over Time (km)', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Distance (km)', fontsize=12)
    plt.xticks(rotation=45)
    
    # Annotate the bars with the exact value
    for p in bar_plot.patches:
        bar_plot.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                          ha='center', va='center', fontsize=10, color='black', xytext=(0, 8), 
                          textcoords='offset points')
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    # Bar plot for duration of activities over time
    plt.figure(figsize=(12, 6))
    bar_plot = sns.barplot(x='activity_date', y='duration_minutes', data=df, palette='Reds_d')
    plt.title('Duration of Activities Over Time (minutes)', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Duration (minutes)', fontsize=12)
    plt.xticks(rotation=45)
    
    # Annotate the bars with the exact value
    for p in bar_plot.patches:
        bar_plot.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                          ha='center', va='center', fontsize=10, color='black', xytext=(0, 8), 
                          textcoords='offset points')
    
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# 5. Main function to log activities and visualize progress
def main():
    create_database()
    
    while True:
        print("\nFitness Tracker Menu:")
        print("1. Log Activity")
        print("2. Visualize Progress")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            log_activity()  # Log new activity
        elif choice == '2':
            visualize_progress()  # Visualize progress
        elif choice == '3':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
