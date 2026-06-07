import datetime

def handle_command(command, speak_func):
    """
    Handles time and date related commands.
    Returns True if the command was handled, False otherwise.
    """
    if "time" in command:
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        speak_func(f"The current time is {current_time}")
        return True
        
    elif "date" in command:
        now = datetime.datetime.now()
        current_date = now.strftime("%B %d, %Y")
        speak_func(f"Today's date is {current_date}")
        return True
        
    return False
