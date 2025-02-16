# src/appointments.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from plyer import notification
import csv
import time
from threading import Thread
from src import speak_handler
from tkcalendar import Calendar
import sqlite3

def save_appointment(doctor_name, app_date, app_time):
    """Save appointment to SQLite database"""
    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO appointments (doctor_name, appointment_date, appointment_time)
                      VALUES (?, ?, ?)''', (doctor_name, app_date, app_time))
    
    conn.commit()
    conn.close()
    print(f"Appointment for {doctor_name} saved successfully!")


def load_appointments():
    """Load all appointments from the database"""
    appointments = []
    try:
        conn = sqlite3.connect('appointments.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, doctor_name, appointment_date, appointment_time, reminder_sent FROM appointments')
        
        for row in cursor.fetchall():
            appointments.append({
                "id": row[0],
                "doctor_name": row[1],
                "appointment_date": row[2],
                "appointment_time": row[3],
                "reminder_sent": row[4]  # Make sure reminder_sent is fetched
            })
        
        conn.close()
    except sqlite3.Error as e:
        print(f"Error loading appointments: {e}")
    
    return appointments

# Function to convert user input time to a standardized format (HH:MM 24-hour)
def convert_to_24hr_format(hour, minute):
    """Convert selected hour and minute to a 24-hour format (HH:MM)"""
    return f"{hour:02d}:{minute:02d}"

# Function to send appointment reminder notification
def send_appointment_reminder(doctor_name, app_date, app_time):
    """Send a desktop notification for the doctor's appointment reminder"""
    notification.notify(
        title=f"Appointment Reminder with {doctor_name}",
        message=f"Your appointment with Dr. {doctor_name} is scheduled on {app_date} at {app_time}",
        timeout=10  # Duration of the notification
    )
    print(f"Notification sent for appointment with {doctor_name}!")
    speak_handler.speak(f"Your appointment with Dr. {doctor_name} is scheduled on {app_date} at {app_time}")

def mark_appointment_as_sent(appointment_id):
    """Mark the appointment reminder as sent"""
    try:
        conn = sqlite3.connect('appointments.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE appointments
                          SET reminder_sent = 1
                          WHERE id = ?''', (appointment_id,))
        
        conn.commit()
        conn.close()
        print(f"Appointment reminder marked as sent for ID: {appointment_id}")
    except sqlite3.Error as e:
        print(f"Error marking appointment as sent: {e}")

def check_appointments():
    """Check if current time matches any appointment time, only if the reminder has not already been sent"""
    while True:
        current_time = time.strftime("%H:%M")  # Get current time in HH:MM format
        current_date = time.strftime("%Y-%m-%d")  # Get current date in YYYY-MM-DD format
        print(f"Current Date and Time: {current_date} {current_time}")  # Debugging

        appointments = load_appointments()  # Load appointments from database
        
        for appointment in appointments:
            app_time = appointment["appointment_time"]
            app_date = appointment["appointment_date"]
            reminder_sent = appointment["reminder_sent"]  # Check if the reminder has been sent
            
            print(f"Checking Appointment with Dr. {appointment['doctor_name']} - Date: {app_date}, Time: {app_time}, Sent: {reminder_sent}")  # Debugging

            # Only check and send the reminder if it hasn't been sent
            if reminder_sent == 0:  # Only proceed if reminder has not been sent
                if current_date == app_date and current_time == app_time:
                    # If current date and time match the appointment date and time, send a reminder
                    send_appointment_reminder(appointment["doctor_name"], app_date, app_time)
                    
                    # After sending the reminder, mark it as sent
                    mark_appointment_as_sent(appointment["id"])  # Update the reminder_sent field to 1
        
        time.sleep(60)  # Check every 60 seconds


# Function to open the appointment window and set appointment reminder
def open_appointments_window():
    appointment_window = tk.Toplevel()
    appointment_window.title("Doctor's Appointments")
    
    # Entry fields for appointment details
    tk.Label(appointment_window, text="Doctor's Name").pack()
    doctor_name = tk.Entry(appointment_window)
    doctor_name.pack()

    # Calendar for date selection
    tk.Label(appointment_window, text="Select Date").pack()
    cal = Calendar(appointment_window, selectmode="day", date_pattern="yyyy-mm-dd")  # Calendar widget
    cal.pack()

    # Time picker (Hour)
    tk.Label(appointment_window, text="Hour").pack()
    hour_combobox = ttk.Combobox(appointment_window, values=[f"{i:02d}" for i in range(24)], state="readonly")
    hour_combobox.set("00")  # Default hour value (8 AM)
    hour_combobox.pack()

    # Time picker (Minute)
    tk.Label(appointment_window, text="Minute").pack()
    minute_combobox = ttk.Combobox(appointment_window, values=[f"{i:02d}" for i in range(60)], state="readonly")
    minute_combobox.set("00")  # Default minute value
    minute_combobox.pack()

    def set_appointment():
        # Get the details of the appointment
        doctor = doctor_name.get()
        date = cal.get_date() 
        hour = int(hour_combobox.get())  # Get selected hour
        minute = int(minute_combobox.get())  # Get selected minute
        
        # Convert the time to a 24-hour format (HH:MM)
        appointment_time = convert_to_24hr_format(hour, minute)
        
        # Save the appointment details to a CSV file
        save_appointment(doctor, date, appointment_time)
        
        # Send an immediate notification for testing purposes (optional)
        notification.notify(
            title="Appointment Reminder",
            message=f"Your appointment with Dr. {doctor} is on {date} at {appointment_time}",
            timeout=10
        )
        
        messagebox.showinfo("Appointment Set", f"Appointment set with Dr. {doctor} on {date} at {appointment_time}")
        appointment_window.destroy()

    tk.Button(appointment_window, text="Set Appointment", command=set_appointment).pack()

# Start the background appointment checking when the app runs
def start_appointment_checking():
    appointment_thread = Thread(target=check_appointments, daemon=True)
    appointment_thread.start()

def create_appointments_database():
    """Create a database and tables if they don't exist"""
    conn = sqlite3.connect('appointments.db')  # Connect to SQLite DB
    cursor = conn.cursor()
    
    # Create table for appointments with reminder_sent field
    cursor.execute('''CREATE TABLE IF NOT EXISTS appointments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        doctor_name TEXT,
                        appointment_date TEXT,
                        appointment_time TEXT,
                        reminder_sent INTEGER DEFAULT 0)''')

    conn.commit()
    conn.close()

# Call the function at the start of the program to create the database
create_appointments_database()

start_appointment_checking()