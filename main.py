from ui import start_ui
from brain import think

def handle_message(text):
    return think(text)

start_ui(handle_message)
