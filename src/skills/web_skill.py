import wikipedia
import requests

def handle_command(command, speak_func):
    """
    Handles web-based queries like Wikipedia searches and Weather.
    Returns True if the command was handled, False otherwise.
    """
    if "wikipedia" in command or "who is" in command or "what is" in command:
        # Extract the topic from the command
        topic = command.replace("wikipedia", "").replace("search", "").replace("who is", "").replace("what is", "").strip()
        
        if topic:
            speak_func(f"Searching Wikipedia for {topic}...")
            try:
                # Fetch a short summary (2 sentences)
                summary = wikipedia.summary(topic, sentences=2)
                speak_func("According to Wikipedia:")
                speak_func(summary)
            except wikipedia.exceptions.DisambiguationError as e:
                speak_func("There are too many results for that topic. Please be more specific.")
            except wikipedia.exceptions.PageError:
                speak_func("I couldn't find any information on that topic.")
            except Exception:
                speak_func("I had trouble connecting to Wikipedia right now.")
        else:
            speak_func("What do you want me to search on Wikipedia?")
        return True

    elif "weather" in command:
        speak_func("Checking the current weather...")
        try:
            # Using wttr.in for a simple, free weather readout
            # The format string %l (location), %C (condition), %t (temperature)
            response = requests.get('https://wttr.in/?format=%l:+%C,+with+a+temperature+of+%t')
            if response.status_code == 200:
                weather_info = response.text.replace("+", "")
                speak_func(f"The current weather is: {weather_info}")
            else:
                speak_func("I couldn't fetch the weather right now.")
        except Exception:
            speak_func("I had trouble connecting to the weather service.")
        return True
    
    return False
