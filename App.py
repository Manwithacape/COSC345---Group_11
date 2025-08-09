import eel
import tkinter as tk
from tkinter import filedialog

# Initialize the eel web folder
eel.init('web')

@eel.expose
def add_numbers(a, b):
    """Function to add two numbers."""
    return a + b

@eel.expose
def open_file():
    """open a file dialog to select a file and return the file path."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    if file_path:
        return file_path
    else:
        return "No file selected"


if __name__ == '__main__':
    eel.start('index.html', size=(800, 600))