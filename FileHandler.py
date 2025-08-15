## ------ IMPORTS ------ ##
import os
import tkinter as tk
import json
from tkinter import filedialog
from datetime import datetime

class FileHandler:
    """Class to handle file operations for the PhotoSIFT application."""

    def __init__(self):
        self.root_dir = os.path.expanduser('~')
        self.photoSIFT_dir = self.create_directory(os.path.join(self.root_dir, 'PhotoSIFT'))
        self.Collections_dir = self.create_directory(os.path.join(self.photoSIFT_dir, 'Collections'))
    
    def create_directory(self, directory_name):
        """Create a directory if it does not exist."""
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        return directory_name
    
    def create_collection(self, collection_name, colletion_description, collection_source):
        """Create a new collection directory and a default JSON file."""
        print(f"Creating collection: {collection_name}")
        collection_path = os.path.join(self.Collections_dir, collection_name)
        new_collection_path = self.create_directory(collection_path)
        
        # Create a default JSON file for the collection
        default_data = {
            "name": collection_name, 
            "description": colletion_description,
            "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source": collection_source,
            "photos": self.get_files(collection_source, include_subdirs=True, file_types=['.jpg', '.png', '.jpeg'])
        }
        json_file_path = os.path.join(new_collection_path, 'collection.json')
        self.write_json(default_data, json_file_path)
        
    def write_json(self, data, file_path):
        """Write data to a JSON file."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)


    ## static methods for file dialog operations
    @staticmethod
    def open_file_dialog(selection_type='file'):
        """Open a file dialog to select a file or directory."""
        root = tk.Tk()
        root.withdraw()
        if selection_type == 'file':
            file_path = filedialog.askopenfilename()
        elif selection_type == 'directory':
            file_path = filedialog.askdirectory()
        else:
            raise ValueError("Invalid selection type. Use 'file' or 'directory'.")
        return file_path
    
    @staticmethod
    def get_files(path, include_subdirs=False, file_types=None):
        """Get all files in a directory."""
        if not os.path.exists(path):
            raise FileNotFoundError(f"The path {path} does not exist.")
        
        files = []
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                if file_types is None or any(filename.endswith(ext) for ext in file_types):
                    files.append(os.path.join(root, filename))
            if not include_subdirs:
                break
        return files