## PhotoSIFT Application - Main Application File
## This file initializes the Eel application and exposes functions for file handling and collection management.
## ------ IMPORTS ------ ##
import os
import base64
import eel
import tkinter as tk
from tkinter import filedialog

import FileHandler as fh
import PhotoAnalysis as Analysis

FileHandler = fh.FileHandler()

## ------ EEL EXPOSED FUNCTIONS ------ ##
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
    """ 
    THIS IS IMPORTANT FOR THE DASHBOARD TO DISPLAY IMAGES WEB PAGES
    CHROME DOES NOT SUPPORT LOCAL FILES, SO WE CONVERT THEM TO BASE64 DATA URLS THEN PASS THEM TO THE FRONTEND
    """
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

## ------ MAIN FUNCTION ------ ##
if __name__ == '__main__':
    eel.init('web')
    eel.start('dashboard.html', size=(1920, 1080))