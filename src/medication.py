# src/medication.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from plyer import notification
import csv
import time
from threading import Thread
import sqlite3

# Function to save medication reminder
def save_medication(medication_name, dose, reminder_time):
    """Save medication reminder to SQLite database"""
    conn = sqlite3.connect('medications.db')
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO medications (medication_name, dose, reminder_time)
                      VALUES (?, ?, ?)''', (medication_name, dose, reminder_time))
    
    conn.commit()
    conn.close()
    print(f"Reminder for {medication_name} saved successfully!")

# Function to load all medication reminders
def load_medications():
    """Load all medication reminders from the database"""
    medications = []
    try:
        conn = sqlite3.connect('medications.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, medication_name, dose, reminder_time, reminder_sent FROM medications')
        
        for row in cursor.fetchall():
            medications.append({
                "id": row[0],
                "medication_name": row[1],
                "dose": row[2],
                "reminder_time": row[3],
                "reminder_sent": row[4]
            })
        
        conn.close()
    except sqlite3.Error as e:
        print(f"Error loading medications: {e}")
    
    return medications

def convert_to_24hr_format(hour, minute):
    """Convert selected hour and minute to a 24-hour format (HH:MM)"""
    return f"{hour:02d}:{minute:02d}"

# Function to send medication reminder notification
def send_medication_reminder(medication_name, dose, reminder_time):
    """Send a desktop notification for the medication reminder"""
    notification.notify(
        title=f"Time to take {medication_name}",
        message=f"Take {dose} of {medication_name} at {reminder_time}",
        timeout=10  # Duration of the notification
    )
    print(f"Notification sent for {medication_name}!")


def mark_reminder_as_sent(medication_id):
    """Update the reminder_sent field to 1 after sending the reminder"""
    conn = sqlite3.connect('medications.db')
    cursor = conn.cursor()
    
    cursor.execute('''UPDATE medications
                      SET reminder_sent = 1
                      WHERE id = ?''', (medication_id,))
    
    conn.commit()
    conn.close()

# Function to check and trigger notifications for medication reminders
def check_reminders():
    """Check if current time matches any reminder time, only if the reminder has not already been sent"""
    while True:
        current_time = time.strftime("%H:%M")
        print(f"Current Time: {current_time}")  # Get current time in HH:MM format
        medications = load_medications()  # Load medication reminders from database
        
        for medication in medications:
            reminder_time = medication["reminder_time"]
            reminder_sent = medication["reminder_sent"]  # Check if the reminder has been sent
            
            print(f"Checking Medication: {medication['medication_name']} - Reminder Time: {reminder_time}, Sent: {reminder_sent}")
            
            if reminder_sent == 0:  # Only check reminder time if reminder has not been sent yet
                if current_time == reminder_time:
                    # If current time matches the reminder time, send a notification
                    send_medication_reminder(medication["medication_name"], medication["dose"], reminder_time)
                    
                    # After sending the reminder, mark it as sent
                    mark_reminder_as_sent(medication["id"])  # Update the reminder_sent field to 1
        
        time.sleep(60)  # Check every 60 seconds


# Function to start the reminder checking in a separate thread
def start_reminder_checking():
    print(f"Starting Reminder check") 
    reminder_thread = Thread(target=check_reminders, daemon=True)
    reminder_thread.start()

# Function to open the medication reminder window
def open_medication_window():
    medication_window = tk.Toplevel()
    medication_window.title("Medication Reminders")
    
    # Entry fields for medication details
    tk.Label(medication_window, text="Medication Name").pack()
    med_name = tk.Entry(medication_window)
    med_name.pack()
    
    tk.Label(medication_window, text="Dose").pack()
    med_dose = tk.Entry(medication_window)
    med_dose.pack()

    # Time picker (Hour)
    tk.Label(medication_window, text="Hour").pack()
    hour_combobox = ttk.Combobox(medication_window, values=[f"{i:02d}" for i in range(24)], state="readonly")
    hour_combobox.set("00")  # Default hour value (8 AM)
    hour_combobox.pack()

    # Time picker (Minute)
    tk.Label(medication_window, text="Minute").pack()
    minute_combobox = ttk.Combobox(medication_window, values=[f"{i:02d}" for i in range(60)], state="readonly")
    minute_combobox.set("00")  # Default minute value
    minute_combobox.pack()

    def set_reminder():
        medication = med_name.get()
        dose = med_dose.get()
        hour = int(hour_combobox.get())
        minute = int(minute_combobox.get())

        reminder_time = convert_to_24hr_format(hour, minute)
        
        # Save the medication reminder to a CSV file
        save_medication(medication, dose, reminder_time)
        
        # Send an immediate notification for testing purposes (optional)
        notification.notify(
            title="Medication Reminder",
            message=f"Time to take {dose} of {medication} at {time}",
            timeout=10
        )
        
        messagebox.showinfo("Reminder Set", f"Reminder set for {medication} at {time}")
        medication_window.destroy()

    tk.Button(medication_window, text="Set Reminder", command=set_reminder).pack()

def create_database():
    """Create a database and tables if they don't exist"""
    conn = sqlite3.connect('medications.db')  # Connect to SQLite DB
    cursor = conn.cursor()
    
    # Create table for medications with reminder_sent field
    cursor.execute('''CREATE TABLE IF NOT EXISTS medications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        medication_name TEXT,
                        dose TEXT,
                        reminder_time TEXT,
                        reminder_sent INTEGER DEFAULT 0)''')  # reminder_sent is 0 by default

    conn.commit()
    conn.close()

    conn.close()

# Call the function at the start of the program to create the database
create_database()


# Start the background reminder checking when the app runs
start_reminder_checking()