## ------ IMPORTS ------ ##
import os
import tkinter as tk
from tkinter import filedialog

## ------ FILE HANDLE FUNCTION ------ ##
def structure_data_directory():
    """
    Structures the data directory by creating necessary subdirectories.
    
    :return: The path to the collections directory.
    """
    data_dir = get_data_directory()

    # Create or find a directory for storing collections called 'collections'
    collections_dir = find_or_create_directory(os.path.join(data_dir, 'collections'))

    # Create or find a directory for storing settings called 'settings'
    settings_dir = find_or_create_directory(os.path.join(data_dir, 'settings'))

    return data_dir 

## ------ HELPER FUNCTIONS ------ ##
def get_data_directory():
    """
    Gets the root directory for the application and creates a data directory if it doesn't exist.
    
    :return: The path to the data directory.
    """
    # Get the user's home directory
    root_dir = os.path.expanduser('~')

    # Create or find a directory for storing data called 'photoreview'
    data_dir = find_or_create_directory(os.path.join(root_dir, 'photoreview'))

    return data_dir

def find_or_create_directory(_path):
    """
    Finds or creates a directory at the specified path.
    
    :param _path: The path to the directory.
    :return: The path to the directory.
    """
    if not os.path.exists(_path):
        os.makedirs(_path)
    return _path

def select_directory():
    """
    Opens a file dialog to select a directory and returns the selected path.
    
    :return: The path to the selected directory.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    directory_path = filedialog.askdirectory(title="Select Directory")
    
    if directory_path:
        return directory_path
    else:
        return None