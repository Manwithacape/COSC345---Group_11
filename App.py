## ------ OTHER PROJECT FILES ------ ##
import PhotoAnalysis as Analysis
import FileHandle as FileHandler

## ------ IMPORTS AND EEL SET UP ------ ##
import eel
import os
import sys
import tkinter as tk
from tkinter import filedialog
import db

# Initialize the eel web folder
eel.init('web')

## ------ EEL EXPOSED FUNCTIONS ------ ##
## Create exposed wrapper functions for Eel to call from JavaScript
@eel.expose
def onStart():
    # db connect
    db.init_db()

    # Continue with file system setup
    root_dir = os.path.expanduser('~')
    print(f"Root directory: {root_dir}")
    
    ## get the users root directory i.e. c:\Users\<username>\documents 
    root_dir = os.path.expanduser('~')
    print(f"Root directory: {root_dir}")

    ## create or find a direcory for storing data called photoreview 
    PhotoSIFT_dir = find_or_create_directory(os.path.join(root_dir, 'PhotoSIFT'));

    ## create or find a directory for called user in the PhotoSIFT directory
    user_dir = find_or_create_directory(os.path.join(PhotoSIFT_dir, 'user'));

    ## if there is no users.json file, create it
    users_file = os.path.join(user_dir, 'users.json')
    if not os.path.exists(users_file):
        with open(users_file, 'w') as f:
            f.write('{}')

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

## ------ HELPER FUNCTIONS ------ ##

def find_or_create_directory(_directory_name):
    """Find or create a directory with the given name."""
    if not os.path.exists(_directory_name):
        os.makedirs(_directory_name)

    return _directory_name

## ------ MAIN EXECUTION ------ ##
if __name__ == '__main__':
    # Set the app icon (toolbar icon) for the Eel window
    eel.start('index.html', size=(800, 600), )