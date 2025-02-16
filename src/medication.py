# src/medication.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from plyer import notification
import csv
import time
from threading import Thread
import sqlite3
import speech_recognition as sr
from src import speak_handler

recognizer = sr.Recognizer()
mic = sr.Microphone()

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
                    speak_handler.speak(f"It's time to take {medication['dose']} of {medication['medication_name']}")
                    
                    # After sending the reminder, mark it as sent
                    mark_reminder_as_sent(medication["id"])  # Update the reminder_sent field to 1
        
        time.sleep(60)  # Check every 60 seconds


# Function to start the reminder checking in a separate thread
def start_reminder_checking():
    print(f"Starting Reminder check") 
    reminder_thread = Thread(target=check_reminders, daemon=True)
    reminder_thread.start()


# Function to listen to voice input with retries
def listen_for_input(prompt):
    retries = 5
    while retries > 0:
        speak_handler.speak(prompt)
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
            audio = recognizer.listen(source, timeout=20, phrase_time_limit=20)
        
        try:
            command = recognizer.recognize_google(audio, language="en-US")
            speak_handler.speak(f"Recognized Command: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak_handler.speak("Sorry, I couldn't understand that. Please try again.")
        except sr.RequestError as e:
            speak_handler.speak(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            speak_handler.speak(f"An error occurred: {e}")
        
        retries -= 1  # Decrement retries

    speak_handler.speak("Sorry, I couldn't understand after several attempts.")
    return None

def listen_for_time_input():
    time_input = listen_for_input("At what time do you want to take the medication? Please say the time in the format of hour and minute, like 'eight thirty' or 'three fifteen'. Only use hours from 1 to 12.")
    
    if time_input:
        # Split the input into words like "eight" and "thirty"
        time_parts = time_input.split()

        # Initialize hour and minute variables
        hour = 0
        minute = 0

        # Word-to-number dictionary for hours and minutes
        word_to_number = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
            "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
            "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
            "eighteen": 18, "nineteen": 19, "twenty": 20,
            "twenty-one": 21, "twenty-two": 22, "twenty-three": 23, "twenty-four": 24,
            "twenty-five": 25, "twenty-six": 26, "twenty-seven": 27, "twenty-eight": 28, "twenty-nine": 29,
            "thirty": 30, "thirty-one": 31, "thirty-two": 32, "thirty-three": 33, "thirty-four": 34,
            "thirty-five": 35, "thirty-six": 36, "thirty-seven": 37, "thirty-eight": 38, "thirty-nine": 39,
            "forty": 40, "forty-one": 41, "forty-two": 42, "forty-three": 43, "forty-four": 44,
            "forty-five": 45, "forty-six": 46, "forty-seven": 47, "forty-eight": 48, "forty-nine": 49,
            "fifty": 50, "fifty-one": 51, "fifty-two": 52, "fifty-three": 53, "fifty-four": 54,
            "fifty-five": 55, "fifty-six": 56, "fifty-seven": 57, "fifty-eight": 58, "fifty-nine": 59
        }

        # Try to convert the words into numbers
        if len(time_parts) == 2:  # e.g., "eight thirty"
            hour_word = time_parts[0].lower()
            minute_word = time_parts[1].lower()

            # Convert words to numbers
            hour = word_to_number.get(hour_word, 0)
            minute = word_to_number.get(minute_word, 0)

        elif len(time_parts) == 1:  # If only hour is given (e.g., "eight")
            hour_word = time_parts[0].lower()
            hour = word_to_number.get(hour_word, 0)
            minute = 0  # Default to 0 minutes if only hour is spoken

        # Restrict to 12-hour format (hours between 1 and 12)
        if hour < 1 or hour > 12:
            speak_handler.speak("Please provide a valid hour between 1 and 12.")
            return None, None

        return hour, minute
    else:
        return None, None


def listen_for_medication_details():
    # Step 1: Ask for Medication Name
    medication_name = listen_for_input("Please say the name of the medication.")

    # Step 2: Ask for Dose
    dose = listen_for_input("Please say the dose of the medication.")

    # Step 3: Ask for Hour
    hour,minute = listen_for_time_input()
    
    if medication_name and dose and hour and minute:
        speak_handler.speak(f"Got it. You want to take {dose} of {medication_name} at {hour} hr {minute} minutes.")
        reminder_time = convert_to_24hr_format(hour, minute)
        save_medication(medication_name, dose, reminder_time)
    else:
        speak_handler.speak("Sorry, I couldn't understand the full medication details. Please try again.")
        return None, None, None


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