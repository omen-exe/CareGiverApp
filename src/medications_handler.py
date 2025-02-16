import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

from src.data_handler import display_data_in_table

def get_reminded_medications():
    """Fetch and display reminded medications."""
    try:
        conn = sqlite3.connect('medications.db')
        cursor = conn.cursor()
        cursor.execute('SELECT medication_name, dose, reminder_time FROM medications WHERE reminder_sent = 1')
        reminded_medications = cursor.fetchall()
        conn.close()
        if reminded_medications:
            display_data_in_table(reminded_medications, ["Medication Name", "Dose", "Reminder Time"], "Reminded Medications")
        else:
            messagebox.showinfo("No Data", "No medications have been reminded yet.")
    except sqlite3.Error as e:
        print(f"Error fetching reminded medications: {e}")

def get_upcoming_medications():
    """Fetch and display upcoming medications."""
    try:
        conn = sqlite3.connect('medications.db')
        cursor = conn.cursor()
        cursor.execute('SELECT medication_name, dose, reminder_time FROM medications WHERE reminder_sent = 0')
        upcoming_medications = cursor.fetchall()
        conn.close()
        if upcoming_medications:
            display_data_in_table(upcoming_medications, ["Medication Name", "Dose", "Reminder Time"], "Upcoming Medications")
        else:
            messagebox.showinfo("No Data", "No upcoming medications found.")
    except sqlite3.Error as e:
        print(f"Error fetching upcoming medications: {e}")


def open_medications_options():
    """Open a window with options for medications (reminded or upcoming)."""
    options_window = tk.Toplevel()
    options_window.title("Medications Options")
    
    tk.Button(options_window, text="Get Already Reminded Medications", command=get_reminded_medications).pack(pady=10)
    tk.Button(options_window, text="Get Upcoming Medications", command=get_upcoming_medications).pack(pady=10)
