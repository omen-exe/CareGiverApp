import pyttsx3

def speak(text):
    """Speak out the text."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()