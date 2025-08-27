## App.py
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
from PhotoAnalysis import PhotoAnalyzer
import db
from db import Camera  # <-- Add this import

## Initialize Helper Classes
FileHandler = FileHandler()
db_instance = db.Database()

## ------ EEL EXPOSED FUNCTIONS ------ ##
## Create exposed wrapper functions for Eel to call from JavaScript
@eel.expose
def onStart():
    """
    Initialize the application and database, print startup info, and handle errors gracefully.
    """
    print("Frontend (Re)loading...")

@eel.expose
def create_collection(collection_name, colletion_description, collection_source):
    """ 
    Wrapper function to create a new collection using the FileHandler class.

    Args:
        collection_name (str): The name of the collection.
        colletion_description (str): A description of the collection.
        collection_source (str): The source path for the collection.
    """
    FileHandler.create_collection(
                                  user_id=1,  # Assuming a default user_id for now
                                  collection_name=collection_name, 
                                  colletion_description=colletion_description,
                                  collection_source=collection_source)

@eel.expose # Function to create a new camera entry in the database
def create_camera(camera_name, camera_make, camera_model,
                  lens_make, lens_model, aperture, shutter_speed, iso, photo_path):
    """ Wrapper function to create a new camera entry in the database.
    Args:
        camera_name (str): Name of the camera.
        camera_make (str): Make of the camera.
        camera_model (str): Model of the camera.
        lens_make (str): Make of the lens.
        lens_model (str): Model of the lens.
        aperture (float): Aperture value.
        shutter_speed (float): Shutter speed value.
        iso (int): ISO value.
        photo_path (str): Path to the photo associated with the camera.
    Returns:
        dict: A dictionary containing the success status and the created camera entry."""
    camera_model_instance = Camera(db_instance)  
    row = camera_model_instance.create(
        camera_name=camera_name,
        camera_make=camera_make,
        camera_model=camera_model,
        lens_make=lens_make,
        lens_model=lens_model,
        aperture=aperture,
        shutter_speed=shutter_speed,
        iso=iso,
        photo_path=photo_path
    )
    return {"success": bool(row), "camera": row}

@eel.expose #Function used to get all the cameras from the database
def list_cameras():
    """ 
    Wrapper function to list all cameras from the database.
    Returns:
        list: of all cameras in the database. 
    """
    camera_model_instance = Camera(db_instance)
    return camera_model_instance.list_all() 
      
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
def select_file(selection_type='file'):
    """
    Wrapper function to open a file dialog for selecting a file.
    Args:
        selection_type (str): Type of selection, either 'file' or 'directory'.

    Returns:
        str: The path of the selected file.
    """
    return FileHandler.open_file_dialog(selection_type)

@eel.expose
def get_all_collections():
    """
    Wrapper function to get all collections from the FileHandler class.
    Returns: 
        list: A list of dictionaries containing collection information.
    """
    return FileHandler.get_all_collections()

@eel.expose
def get_image_data_url(image_path):
    """
    Convert an image file to a base64 data URL for display in the web application.
    Args:
        image_path (str): The path to the image file.
        
    Returns:
    str: A base64 data URL representing the image.
    """
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

## ------ App Initialization ------ ##
def backend_init():
    """
    Initialize backend components such as the database and print startup information.
    """
    print("Backend initializing...")

    # Try to connect to the database
    try:
        db_instance.init_db()
        print("  Database initialized successfully.")
    except Exception as e:
        print(f"  Database initialization failed: {e}")

    # Create a file handler instance
    file_handler = FileHandler
    print(f"  Data Directory: {FileHandler.photoSIFT_dir}")

def frontend_init(size=(1920, 1080), mode='chrome'):
    """
    Initialize frontend components and print relevant information.
    Args:
        size (tuple): The size of the Eel window.
        mode (str): The mode to run Eel in (e.g., 'chrome', 'edge', etc.).
    """
    print("Frontend starting...")
    eel.init('web')
    eel.start('dashboard.html', size=size, mode=mode)

## ------ MAIN FUNCTION ------ ##
if __name__ == '__main__':
   backend_init()
   frontend_init()