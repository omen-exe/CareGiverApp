# main.py
from src.voice_activation import ask_to_activate_voice_command

# Main function to start app
def start_app():
    # Ask the user if they want to activate voice command via speech recognition
    ask_to_activate_voice_command()

if __name__ == "__main__":
    start_app()
