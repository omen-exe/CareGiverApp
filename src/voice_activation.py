
import speech_recognition as sr

from src import speak_handler
from src.app import main_app
from src.medication import listen_for_medication_details
from src.appointments import open_appointments_window
from src.health_metrics import open_health_window

MAX_RETRIES = 5


def handle_retry(retries, action):
    """Handle retry logic."""
    if retries < MAX_RETRIES:
        speak_handler.speak(f"You have {MAX_RETRIES - retries} attempts remaining.")
        action(retries + 1)
    else:
        speak_handler.speak("Sorry, I couldn't understand after multiple attempts. Proceeding with default actions.")
        main_app()


def ask_to_activate_voice_command():
    """Ask the user if they want to activate the voice command."""
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    try:
        with mic as source:
            print("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
            print("Please say 'Yes' or 'No' to activate voice command.")
            speak_handler.speak("Do you want to activate voice command? Please say yes or no.")
            
            # Start listening with a timeout
            audio = recognizer.listen(source, timeout=20, phrase_time_limit=10)  # Timeout after 10 seconds if no speech
            print("Listening finished.")
        
        # Attempt to recognize speech using Google's speech recognition API
        command = recognizer.recognize_google(audio, language="en-US")
        print(f"Recognized Command: {command}")
        command = command.lower()

        if "yes" in command:
            speak_handler.speak("Activating voice command.")
            listen_for_commands()  # Start listening for voice commands
        elif "no" in command:
            speak_handler.speak("Proceeding with the app without voice command.")
            main_app()  # Open the app without voice commands
        else:
            speak_handler.speak("Sorry, I didn't understand. Please say 'Yes' or 'No'.")
            ask_to_activate_voice_command()  # Retry if the answer is unclear

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
        speak_handler.speak("Sorry, I couldn't understand the command. Please try again.")
        ask_to_activate_voice_command()  # Retry if speech recognition fails

    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        speak_handler.speak("Sorry, there was an issue with the service. Please try again.")
        main_app()  # Proceed with the app in case of an error
    
    except Exception as e:
        print(f"An error occurred: {e}")
        speak_handler.speak("An unexpected error occurred. Please try again.")
        main_app()  # Proceed with the app in case of an error


def listen_for_commands(retries=0):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    while True:  # Run indefinitely
        try:
            with mic as source:
                print("Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
                print("Please wait, listening for your command...")
                speak_handler.speak("Listening for commands now. Please speak.")

                # Announce available commands to the user
                available_commands = "You can say, 'Medication to set a Reminder for medication', 'Appointments to set a reminder for appointments', 'Health Metrics to register the patient's health metrics' or 'quit to quit the application'."
                #speak_handler.speak("Here are the available commands: " + available_commands)
                
                # Start listening with a timeout
                audio = recognizer.listen(source, timeout=20, phrase_time_limit=20)  # Timeout after 5 seconds if no speech
                print("Listening finished.")
            
            # Attempt to recognize speech using Google's speech recognition API
            command = recognizer.recognize_google(audio, language="en-US")
            print(f"Recognized Command: {command}")
            command = command.lower()

            if "quit" in command:
                speak_handler.speak("Exiting the application. Goodbye!")
                break

            if "medication" in command:
                speak_handler.speak("Opening Medication Management")
                listen_for_medication_details()

            elif "appointments" in command:
                speak_handler.speak("Opening Appointments Management")
                open_appointments_window()

            elif "health metrics" in command:
                speak_handler.speak("Tracking Health Metrics")
                open_health_window()

            else:
                speak_handler.speak("Sorry, I didn't understand the command.")
                # Optionally prompt again to see if they want to quit
                speak_handler.speak("Do you want to quit? Say 'Yes' to quit or 'No' to continue.")
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                quit_command = recognizer.recognize_google(audio, language="en-US").lower()
                if "yes" in quit_command:
                    speak_handler.speak("Exiting the application. Goodbye!")
                    break  # Exit the loop if the user wants to quit

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
            speak_handler.speak("Sorry, I couldn't understand the command. Please try again.")
        
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            speak_handler.speak("Sorry, there was an issue with the service. Please try again.")

        except Exception as e:
            print(f"An error occurred: {e}")
            speak_handler.speak("An unexpected error occurred. Please try again.")
