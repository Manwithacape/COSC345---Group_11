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