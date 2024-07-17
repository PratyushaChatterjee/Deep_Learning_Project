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
welcome_text = "Hi, I am a forest monitoring system. I have been made by Shreyan Kundu, Nirban Roy. Please use me to make informed decisions and maximize yields sustainably"

# Wait for 5 seconds
time.sleep(3)

# Speak the welcome message
speak_text(welcome_text)
