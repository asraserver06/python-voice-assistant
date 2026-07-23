import os
import datetime
import webbrowser
import requests
import speech_recognition as sr
import pyttsx3
import winsound
import subprocess
import urllib.parse
import threading
from AppOpener import open as open_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini via REST API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key or api_key == "your_api_key_here":
    print("WARNING: Gemini API key not found or not set. Gemini features will be disabled.")

# Initialize the text-to-speech engine
engine = pyttsx3.init()
# Speed up the talking speed
current_rate = engine.getProperty('rate')
engine.setProperty('rate', current_rate + 35)

# Try to set voice to a female voice (like Zira)
voices = engine.getProperty('voices')
for voice in voices:
    if "zira" in voice.name.lower() or "female" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

def play_ding():
    """Plays a simple beep to indicate it is listening."""
    winsound.MessageBeep(winsound.MB_OK)

def speak(text):
    """Converts text to speech"""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen(quiet=False):
    """Listens to the microphone and returns the spoken text"""
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8 
    
    # Disable dynamic calibration which often breaks on noisy laptops and stops it from hearing you
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 400 # 400 is a solid baseline for normal speaking volume
    
    try:
        with sr.Microphone() as source:
            if not quiet:
                print("\nListening...")
            # Prevent it from hanging forever by adding timeouts
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                return ""
    except (OSError, AttributeError) as e:
        if not quiet:
            print(f"Microphone error: {e}")
        return ""

    try:
        if not quiet:
            print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-US')
        if not quiet:
            print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        if not quiet:
            print("Sorry, I didn't catch that. Could you repeat?")
        return ""
    except sr.RequestError:
        if not quiet:
            print("Network error. Please check your internet connection.")
        return ""

def ask_gemini(prompt):
    """Sends a prompt to Gemini and returns the response using REST API."""
    if not api_key or api_key == "your_api_key_here":
        return "I'm sorry, my Gemini AI is not configured. Please check the API key."
    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": api_key
        }
        data = {
            "contents": [{
                "parts": [{"text": f"You are a helpful voice assistant. Keep your response conversational, short, and to the point. Answer this: {prompt}"}]
            }]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=(5, 30))
        response.raise_for_status() # Raise an error if the request fails
        
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"].strip()
        
    except Exception as e:
        print(f"Gemini error: {e}")
        return "I had trouble connecting to my AI brain."

def process_command(command):
    """Routes the command to the appropriate action."""
    if not command:
        return True # Continue listening

    if command in ["stop", "exit", "goodbye", "quit"]:
        speak("Goodbye! Have a great day.")
        return False # Stop the loop

    elif "what time is it" in command or "current time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")

    elif "what is the date" in command or "today's date" in command:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {current_date}.")

    elif "open youtube" in command:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "open google" in command:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")
        
    elif "search for" in command:
        query = command.split("search for", 1)[-1].strip()
        encoded_query = urllib.parse.quote_plus(query)
        speak(f"Searching Google for {query}.")
        webbrowser.open(f"https://www.google.com/search?q={encoded_query}")

    elif command.startswith("open "):
        app_name = command[5:].strip()
        app_name = app_name.replace("please", "").replace("for me", "").strip()
        
        speak(f"Trying to open {app_name}.")
        
        # Hardcoded aliases for Microsoft products and common apps
        aliases = {
            "word": "winword",
            "ms word": "winword",
            "microsoft word": "winword",
            "excel": "excel",
            "ms excel": "excel",
            "microsoft excel": "excel",
            "powerpoint": "powerpnt",
            "ms powerpoint": "powerpnt",
            "microsoft powerpoint": "powerpnt",
        }
        
        exe_name = aliases.get(app_name, app_name)
        
        # Run AppOpener in a background thread so it doesn't freeze the assistant!
        def open_in_background(original_name, exe_name):
            if original_name in aliases:
                # For known tricky apps like Word/Excel, directly use Windows start
                try:
                    subprocess.run(["start", "", exe_name], shell=True, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Failed to open {exe_name}: {e}")
            else:
                # For everything else, try AppOpener
                try:
                    open_app(original_name, match_closest=False)
                except Exception as e:
                    print(f"Failed to open {original_name}: {e}")
                
        threading.Thread(target=open_in_background, args=(app_name, exe_name)).start()

    else:
        # Fallback to Gemini for general knowledge and conversation
        print("Let me think about that...") # Using print instead of speak to avoid blocking the API call!
        response = ask_gemini(command)
        speak(response)

    return True

if __name__ == "__main__":
    speak("Hello! I am your advanced voice assistant. I am online and ready.")
    print("Say 'Hey Assistant' to wake me up.")
    
    # The Core Loop
    is_running = True
    WAKE_WORD = "hey assistant"

    while is_running:
        # Listen quietly in the background
        user_command = listen(quiet=True)
        
        if user_command:
            # Check if the wake word is spoken
            if user_command.startswith(WAKE_WORD):
                # Remove the wake word to see if they said a command too
                command_after_wake = user_command[len(WAKE_WORD):].strip()
                
                if command_after_wake:
                    # They said a full sentence: "Hey Assistant what time is it"
                    print(f"\nUser said: {user_command}")
                    is_running = process_command(command_after_wake)
                else:
                    # They just said "Hey Assistant"
                    print(f"\nUser said: {user_command}")
                    play_ding()
                    # Listen normally for the actual command
                    actual_command = listen(quiet=False)
                    is_running = process_command(actual_command)
