import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.append(os.path.abspath('src'))
import main

@pytest.fixture(autouse=True)
def mock_dependencies():
    with patch('main.speak') as mock_speak, \
         patch('main.webbrowser.open') as mock_browser, \
         patch('main.winsound.MessageBeep') as mock_beep, \
         patch('main.ask_gemini', return_value="Mocked Gemini Response") as mock_gemini, \
         patch('main.open_app') as mock_open_app, \
         patch('main.threading.Thread') as mock_thread, \
         patch('main.subprocess.run') as mock_subprocess:
        
        # Make the mocked thread execute its target synchronously for testing
        def mock_thread_init(target, args=(), kwargs={}):
            target(*args, **kwargs)
            return MagicMock()
        mock_thread.side_effect = mock_thread_init

        yield {
            'speak': mock_speak,
            'browser': mock_browser,
            'beep': mock_beep,
            'gemini': mock_gemini,
            'open_app': mock_open_app,
            'subprocess': mock_subprocess
        }

def test_time_command(mock_dependencies):
    result = main.process_command("what time is it")
    assert result is True
    mock_dependencies['speak'].assert_called_once()
    assert "The current time is" in mock_dependencies['speak'].call_args[0][0]

def test_date_command(mock_dependencies):
    result = main.process_command("what is the date")
    assert result is True
    mock_dependencies['speak'].assert_called_once()
    assert "Today is" in mock_dependencies['speak'].call_args[0][0]

def test_open_youtube(mock_dependencies):
    result = main.process_command("open youtube")
    assert result is True
    mock_dependencies['browser'].assert_called_with("https://www.youtube.com")

def test_search_command(mock_dependencies):
    result = main.process_command("search for python voice assistant")
    assert result is True
    mock_dependencies['browser'].assert_called_with("https://www.google.com/search?q=python+voice+assistant")

def test_open_app_normal(mock_dependencies):
    result = main.process_command("open calculator")
    assert result is True
    mock_dependencies['open_app'].assert_called_with("calculator", match_closest=False)

def test_open_app_alias(mock_dependencies):
    result = main.process_command("open ms word")
    assert result is True
    mock_dependencies['subprocess'].assert_called_with(["start", "", "winword"], shell=True, check=True)

def test_gemini_fallback(mock_dependencies):
    result = main.process_command("tell me a joke")
    assert result is True
    mock_dependencies['gemini'].assert_called_with("tell me a joke")
    mock_dependencies['speak'].assert_called_with("Mocked Gemini Response")

def test_exit_commands(mock_dependencies):
    assert main.process_command("stop") is False
    assert main.process_command("exit") is False
    assert main.process_command("goodbye") is False
    mock_dependencies['speak'].assert_called_with("Goodbye! Have a great day.")

def test_stop_not_exact_match(mock_dependencies):
    # Should not exit on arbitrary substrings containing stop
    result = main.process_command("don't stop the music")
    assert result is True
