import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

from src.data_handler import display_data_in_table

def get_health_metrics():
    """Fetch and display health metrics."""
    try:
        conn = sqlite3.connect('health_metrics.db')
        cursor = conn.cursor()
        cursor.execute('SELECT patient_name, weight, blood_pressure FROM health_metrics')
        health_metrics = cursor.fetchall()
        conn.close()
        if health_metrics:
            display_data_in_table(health_metrics, ["Patient Name", "Weight", "Blood Pressure"], "Health Metrics")
        else:
            messagebox.showinfo("No Data", "No health metrics found.")
    except sqlite3.Error as e:
        print(f"Error fetching health metrics: {e}")

def open_health_metrics_window():
    """Open the health metrics window."""
    get_health_metrics()