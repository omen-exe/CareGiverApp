import tkinter as tk
from src.display_options import open_details_options
from src.medication import open_medication_window
from src.appointments import open_appointments_window
from src.health_metrics import open_health_window

def main_app():
    root = tk.Tk()
    root.title("Caregiver App")
    root.geometry("1000x1000")
          
    # Buttons for various functionalities
    tk.Button(root, text="Manage Medication", command=open_medication_window).pack(pady=10)
    tk.Button(root, text="Manage Appointments", command=open_appointments_window).pack(pady=10)
    tk.Button(root, text="Track Health Metrics", command=open_health_window).pack(pady=10)

    tk.Button(root, text="Get Stored Details", command=open_details_options).pack(pady=10)

    
    root.mainloop()
