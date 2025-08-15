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
    FileHandler.create_collection(collection_name=collection_name, 
                                  colletion_description=colletion_description,
                                  collection_source=collection_source)
                                  
@eel.expose
def select_directory(selection_type='directory'):
    return FileHandler.open_file_dialog(selection_type)

if __name__ == '__main__':
    # Set the app icon (toolbar icon) for the Eel window
    eel.init('web')
    eel.start('index.html', size=(1920, 1080))