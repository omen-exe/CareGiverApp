import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

from src.data_handler import display_data_in_table

def get_upcoming_appointments():
    """Fetch and display upcoming appointments."""
    try:
        conn = sqlite3.connect('appointments.db')
        cursor = conn.cursor()
        cursor.execute('SELECT doctor_name, appointment_date, appointment_time FROM appointments WHERE reminder_sent = 0')
        upcoming_appointments = cursor.fetchall()
        conn.close()
        if upcoming_appointments:
            display_data_in_table(upcoming_appointments, ["Doctor Name", "Date", "Time"], "Upcoming Appointments")
        else:
            messagebox.showinfo("No Data", "No upcoming appointments found.")
    except sqlite3.Error as e:
        print(f"Error fetching upcoming appointments: {e}")

def get_completed_appointments():
    """Fetch and display completed appointments."""
    try:
        conn = sqlite3.connect('appointments.db')
        cursor = conn.cursor()
        cursor.execute('SELECT doctor_name, appointment_date, appointment_time FROM appointments WHERE reminder_sent = 1')
        completed_appointments = cursor.fetchall()
        conn.close()
        if completed_appointments:
            display_data_in_table(completed_appointments, ["Doctor Name", "Date", "Time"], "Completed Appointments")
        else:
            messagebox.showinfo("No Data", "No completed appointments found.")
    except sqlite3.Error as e:
        print(f"Error fetching completed appointments: {e}")

def open_appointments_options():
    """Open a window with options for appointments (completed or upcoming)."""
    options_window = tk.Toplevel()
    options_window.title("Appointments Options")
    
    tk.Button(options_window, text="Get Completed Appointments", command=get_completed_appointments).pack(pady=10)
    tk.Button(options_window, text="Get Upcoming Appointments", command=get_upcoming_appointments).pack(pady=10)
