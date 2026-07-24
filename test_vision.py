import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from main import analyze_screen

if __name__ == '__main__':
    print("Testing screen summarization...")
    result = analyze_screen()
    print("Result:")
    print(result)
