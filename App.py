import base64
# Expose a function to serve images as base64 data URLs

import eel

@eel.expose
def get_image_data_url(image_path):
    try:
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode('utf-8')
            # Guess mime type from extension
            ext = os.path.splitext(image_path)[1].lower()
            mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png" if ext == ".png" else "image/*"
            return f"data:{mime};base64,{encoded}"
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None
    
import eel
import FileHandler as fh

FileHandler = fh.FileHandler()

# Expose a function to get all collections and their data from FileHandler
@eel.expose
def get_all_collections():
    return FileHandler.get_all_collections()
## ------ OTHER PROJECT FILES ------ ##
import PhotoAnalysis as Analysis
import FileHandler as fh

## ------ IMPORTS AND EEL SET UP ------ ##
import eel
import os
import tkinter as tk
from tkinter import filedialog

FileHandler = fh.FileHandler()

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

if __name__ == '__main__':
    # Set the app icon (toolbar icon) for the Eel window
    eel.init('web')
    eel.start('dashboard.html', size=(1920, 1080))