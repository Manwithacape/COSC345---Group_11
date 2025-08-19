## PhotoSIFT Application - Main Application File
## This file initializes the Eel application and exposes functions for file handling and collection management.
## ------ IMPORTS ------ ##
import os
import base64
import eel
import os
import sys
import tkinter as tk
from tkinter import filedialog
from FileHandler import FileHandler
import db
FileHandler = FileHandler()
# Initialize the eel web folder
eel.init('web')

## ------ EEL EXPOSED FUNCTIONS ------ ##
## Create exposed wrapper functions for Eel to call from JavaScript
@eel.expose
def onStart():
    """Initialize the application and database."""
    print("Application starting...")

    # Print the data directory
    print(f"Data Directory: {FileHandler.photoSIFT_dir}")
    
    # db connect
    database = db.Database()
    database.init_db()


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
def create_collection(collection_name, colletion_description, collection_source):
    """ 
    Wrapper function to create a new collection using the FileHandler class.

    Args:
        collection_name (str): The name of the collection.
        colletion_description (str): A description of the collection.
        collection_source (str): The source path for the collection.
    """
    FileHandler.create_collection(collection_name=collection_name, 
                                  colletion_description=colletion_description,
                                  collection_source=collection_source)
                                  
@eel.expose
def select_directory(selection_type='directory'):

    """
    Wrapper function to open a file dialog for selecting a file or directory.
    Args:
        selection_type (str): Type of selection, either 'file' or 'directory'.

    Returns:
        str: The path of the selected file or directory.
    """
    return FileHandler.open_file_dialog(selection_type)

@eel.expose
def get_all_collections():
    return FileHandler.get_all_collections()

@eel.expose
def get_image_data_url(image_path):
    try:
        dir_path = os.path.dirname(image_path)
        if not os.path.isfile(image_path):
            return None
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode('utf-8')
            ext = os.path.splitext(image_path)[1].lower()
            mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png" if ext == ".png" else "image/*"
            return f"data:{mime};base64,{encoded}"
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None
 
## ------ MAIN FUNCTION ------ ##
if __name__ == '__main__':
    eel.init('web')
    eel.start('dashboard.html', size=(1920, 1080), mode='chrome')