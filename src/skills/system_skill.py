import os

def handle_command(command, speak_func):
    """
    Handles system-level commands like opening applications.
    Returns True if the command was handled, False otherwise.
    """
    if "open notepad" in command:
        speak_func("Opening Notepad")
        os.system("start notepad")
        return True
        
    elif "open calculator" in command:
        speak_func("Opening Calculator")
        os.system("start calc")
        return True
        
    return False
