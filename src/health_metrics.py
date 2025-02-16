# src/health_metrics.py
import tkinter as tk
from tkinter import messagebox
import sqlite3

def open_health_window():
    health_window = tk.Toplevel()
    health_window.title("Health Metrics")
    
    # Entry fields for health data
    tk.Label(health_window, text="Patient Name").pack()
    patient_name = tk.Entry(health_window)
    patient_name.pack()

    tk.Label(health_window, text="Weight (kg)").pack()
    weight = tk.Entry(health_window)
    weight.pack()

    tk.Label(health_window, text="Blood Pressure").pack()
    blood_pressure = tk.Entry(health_window)
    blood_pressure.pack()

    def save_health_data():
        # Save health data to SQLite database
        patient_name_value = patient_name.get()
        weight_value = weight.get()
        blood_pressure_value = blood_pressure.get()
        
        connection = sqlite3.connect('health_metrics.db')
        cursor = connection.cursor()
        cursor.execute('''
        INSERT INTO health_metrics (patient_name, weight, blood_pressure)
        VALUES (?, ?, ?)
        ''', (patient_name_value, weight_value, blood_pressure_value))
        connection.commit()
        connection.close()
        
        messagebox.showinfo("Health Data Saved", "Health data has been saved.")
        health_window.destroy()

    # Button to save the health data
    tk.Button(health_window, text="Save Data", command=save_health_data).pack()


def create_health_metrics_database():
    """Create a SQLite database and table for health metrics"""
    connection = sqlite3.connect('health_metrics.db')  # Database for health metrics
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS health_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        weight REAL,
        blood_pressure TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    connection.commit()
    connection.close()

create_health_metrics_database()

