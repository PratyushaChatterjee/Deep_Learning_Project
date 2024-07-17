import pyttsx3
import time

def speak_text(text):
    # Initialize the pyttsx3 engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed of speech

    # Convert text to speech
    engine.say(text)

    # Run and wait for the speech to finish
    engine.runAndWait()

# Define the welcome text
welcome_text = "YOU HAVE SUCCESSFULLY ENTERED THE PEST DETECTION SEGMENT"

# Wait for 5 seconds
time.sleep(4)

# Speak the welcome message
speak_text(welcome_text)
