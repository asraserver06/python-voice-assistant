# Advanced Python Voice Assistant

A powerful, Siri-like voice assistant built with Python. This assistant utilizes local speech recognition and interfaces with the Gemini AI model to perform a wide variety of advanced tasks, including screen analysis.

## Features

- **Voice Recognition & Text-To-Speech**: Conversational interface using `speech_recognition` and `pyttsx3`.
- **Gemini AI Integration**: Uses Gemini Flash to answer complex questions and hold conversations.
- **Screen Summarization (Vision)**: The assistant can take a picture of your screen and describe it to you when you say *"summarize my screen"* or *"what am I looking at"*.
- **App Opening**: Launches native Windows applications seamlessly.
- **Web Navigation**: Can search Google or open popular web pages like YouTube directly from a voice command.
- **Time & Date**: Readily fetches the current time and date.
- **Smart Sleep Mode**: Runs quietly in the background without freezing, waiting for the wake word (`"hey assistant"`).

## Setup & Installation

1. **Clone the repository** (if you haven't already).
2. **Set up a virtual environment** (recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables**:
   Copy the `.env.example` file to `.env` and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Usage

Start the assistant by running the main script:
```bash
python src/main.py
```

1. Wait for the assistant to announce it is online.
2. Say the wake word: **"Hey Assistant"**.
3. Speak your command! (e.g., *"Hey Assistant, summarize my screen"*).

## Integration

You can easily integrate this voice assistant into your own Python applications or systems. 

To use the core features programmatically without the continuous listening loop, you can import and call the functions directly from `main.py`:

```python
import sys
import os

# Ensure the src directory is in your Python path
sys.path.append(os.path.abspath("src"))
from main import process_command, analyze_screen, speak

# Example: Programmatically trigger the vision feature
description = analyze_screen()
speak(description)

# Example: Programmatically pass a command as text
process_command("what time is it")
```

If you want the assistant to listen in the background of a GUI app (like Tkinter or PyQt), you can run the core loop in a separate `threading.Thread`.

## Contributors

* **ASRA ARSHAD**
* **HAZAM LIAQAT**
