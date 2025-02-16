
import speech_recognition as sr
import pyttsx3

from src.app import main_app
from src.health_metrics_handler import open_health_metrics_window
from src.medication import open_medication_window
from src.appointments import open_appointments_window
from src.health_metrics import open_health_window

def speak(text):
    """Speak out the text."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def ask_to_activate_voice_command():
    """Ask the user if they want to activate the voice command."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    try:
        with mic as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
            print("Please say 'Yes' or 'No' to activate voice command.")
            speak("Do you want to activate voice command? Please say yes or no.")
            
            # Start listening with a timeout
            audio = recognizer.listen(source, timeout=20, phrase_time_limit=10)  # Timeout after 10 seconds if no speech
            print("Listening finished.")
        
        # Attempt to recognize speech using Google's speech recognition API
        command = recognizer.recognize_google(audio, language="en-US")
        print(f"Recognized Command: {command}")
        command = command.lower()

        if "yes" in command:
            speak("Activating voice command.")
            listen_for_commands()  # Start listening for voice commands
        elif "no" in command:
            speak("Proceeding with the app without voice command.")
            main_app()  # Open the app without voice commands
        else:
            speak("Sorry, I didn't understand. Please say 'Yes' or 'No'.")
            ask_to_activate_voice_command()  # Retry if the answer is unclear

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
        speak("Sorry, I couldn't understand the command. Please try again.")
        ask_to_activate_voice_command()  # Retry if speech recognition fails

    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        speak("Sorry, there was an issue with the service. Please try again.")
        main_app()  # Proceed with the app in case of an error
    
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("An unexpected error occurred. Please try again.")
        main_app()  # Proceed with the app in case of an error


def listen_for_commands():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    try:
        with mic as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
            print("Please wait, listening for your command...")
            speak("Listening for commands now. Please speak.")
            
            # Start listening with a timeout
            audio = recognizer.listen(source, timeout=20, phrase_time_limit=20)  # Timeout after 5 seconds if no speech
            print("Listening finished.")
        
        # Attempt to recognize speech using Google's speech recognition API
        command = recognizer.recognize_google(audio, language="en-US")
        print(f"Recognized Command: {command}")
        command = command.lower()

        if "medication" in command:
            speak("Opening Medication Management")
            open_medication_window()

        elif "appointments" in command:
            speak("Opening Appointments")
            open_appointments_window()

        elif "health metrics" in command:
            speak("Tracking Health Metrics")
            open_health_window()

        else:
            speak("Sorry, I didn't understand the command.")
    
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
        speak("Sorry, I couldn't understand the command. Please try again.")
    
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        speak("Sorry, there was an issue with the service. Please try again.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("An unexpected error occurred. Please try again.")