## ------ OTHER PROJECT FILES ------ ##
import PhotoAnalysis as Analysis

## ------ IMPORTS AND EEL SET UP ------ ##
import eel
import os
import tkinter as tk
from tkinter import filedialog

# Initialize the eel web folder
eel.init('web')

## ------ EEL EXPOSED FUNCTIONS ------ ##
@eel.expose
def onStart():
    ## get the users root directory i.e. c:\Users\<username>\documents 
    root_dir = os.path.expanduser('~')
    print(f"Root directory: {root_dir}")


    ## create or find a direcory for storing data called photoreview 
    data_dir = os.path.join(root_dir, 'photoreview')

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    ## Create or find a directory for storing collections called collections
    collections_dir = os.path.join(data_dir, 'collections')
    if not os.path.exists(collections_dir):
        os.makedirs(collections_dir)
    print(f"Data directory initialized at: {data_dir}")
    return "Application started successfully!"

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


## ------ MAIN EXECUTION ------ ##
if __name__ == '__main__':
    eel.start('index.html', size=(800, 600))