import speech_recognition as sr
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Converts text to speech"""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listens to the microphone and returns the spoken text"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        # Adjust for ambient noise before listening to improve accuracy
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        # Using Google's free web-based speech recognition
        query = recognizer.recognize_google(audio, language='en-US')
        print(f"User said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Could you repeat?")
        return ""
    except sr.RequestError:
        print("Network error. Please check your internet connection.")
        return ""

if __name__ == "__main__":
    speak("Hello! I am your new voice assistant. I am online and ready.")
    
    # The Core Loop
    while True:
        command = listen()
        
        # If a command was successfully recognized
        if command:
            if "stop" in command or "exit" in command:
                speak("Goodbye! Shutting down.")
                break
            else:
                # Basic echo response for now
                speak(f"I heard you say: {command}")
