import tkinter as tk

from src.appointments_handler import get_completed_appointments, get_upcoming_appointments
from src.health_metrics_handler import get_health_metrics
from src.medications_handler import get_reminded_medications, get_upcoming_medications

def open_details_options():
    """Open a window with options for appointments (completed or upcoming)."""
    options_window = tk.Toplevel()
    options_window.title("Appointments Options")
    tk.Button(options_window, text="Get Appointments", command=open_appointments_options).pack(pady=10)
    tk.Button(options_window, text="Get Medications", command=open_medications_options).pack(pady=10)
    tk.Button(options_window, text="Get Patient Health Metrics", command=open_health_metrics_window).pack(pady=10)

def open_appointments_options():
    """Open a window with options for appointments (completed or upcoming)."""
    options_window = tk.Toplevel()
    options_window.title("Appointments Options")
    
    tk.Button(options_window, text="Get Completed Appointments", command=get_completed_appointments).pack(pady=10)
    tk.Button(options_window, text="Get Upcoming Appointments", command=get_upcoming_appointments).pack(pady=10)

def open_medications_options():
    """Open a window with options for medications (reminded or upcoming)."""
    options_window = tk.Toplevel()
    options_window.title("Medications Options")
    
    tk.Button(options_window, text="Get Already Reminded Medications", command=get_reminded_medications).pack(pady=10)
    tk.Button(options_window, text="Get Upcoming Medications", command=get_upcoming_medications).pack(pady=10)

def open_health_metrics_window():
    """Open the health metrics window."""
    get_health_metrics()