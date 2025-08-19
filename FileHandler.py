## ------ FILE HANDLER CLASS ------ ##

## ------ IMPORTS ------ ##
import os
import tkinter as tk
import json
import rawpy  # Ensure you have rawpy installed for RAW file handling
import cv2 as cv
import numpy as np
from tkinter import filedialog
from datetime import datetime
from PhotoAnalysis import PhotoAnalyzer  # Import the PhotoAnalyzer class


class FileHandler:
   

    """Class to handle file operations for the PhotoSIFT application."""
    def __init__(self):
        self.root_dir = os.path.expanduser('~')
        self.photoSIFT_dir = self.create_directory(os.path.join(self.root_dir, 'PhotoSIFT'))
        self.Collections_dir = self.create_directory(os.path.join(self.photoSIFT_dir, 'Collections'))
    
    def create_directory(self, directory_name):
        """
        Creates a directory with the specified name if it does not already exist.

        Args:
            directory_name (str): The name or path of the directory to create.

        Returns:
            str: The name or path of the created (or existing) directory.
        """
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        return directory_name
    
    def get_all_collections(self):
        """Find all collection subdirectories and read their collection.json files."""
        collections = []
        if os.path.exists(self.Collections_dir):
            for collection_name in os.listdir(self.Collections_dir):
                collection_path = os.path.join(self.Collections_dir, collection_name)
                json_path = os.path.join(collection_path, 'collection.json')
                if os.path.isfile(json_path):
                    data = self.read_json(json_path)
                    if data:
                        preview = None
                        collections.append({
                            'name': data.get('name', collection_name),
                            'preview': data.get('thumbnail'),
                            'created_on': data.get('created_on', '')
                        })
        return collections
    
    def create_collection(self, collection_name, colletion_description, collection_source):
        """
        Create a new collection directory and a default JSON file.

        Args:
            collection_name (str): The name of the collection.
            colletion_description (str): A description of the collection.
            collection_source (str): The source path for the collection.
        """
        
        # Create a new collection directory
        collection_path = os.path.join(self.Collections_dir, collection_name)
        new_collection_path = self.create_directory(collection_path)
        
        # Create a default JSON file for the collection
        # individual photo data - this is packed into a list and that list is used to create the collection data
        photos_data = []
        photo_files = self.get_files(collection_source, include_subdirs=True)
        for photo in photo_files:
            # Generate a unique preview filename for each photo, including extension
            preview_filename = f"{os.path.basename(photo)}_preview.jpg"
            preview_path = os.path.join(new_collection_path, preview_filename)

            # Normalize paths
            photo = os.path.normpath(photo)
            preview_path = os.path.normpath(preview_path)

            # Save/copy the preview image to preview_path
            self.extract_jpg_from_raw(photo, new_collection_path)  # This will save the preview image
            photos_data.append({
                "source_path": photo,
                "preview_path": preview_path,
                "analysis": {
                    "sharpness": None,
                    "exposure": None,
                    "saturation": None,
                    "contrast": None,
                    "brightness": None,
                    "faces": [],
                    "near-duplicates": []  # Placeholder for near-duplicate images
                }
            })

        # Create collection data 
        collection_data = {
            "name": collection_name, 
            "description": colletion_description,
            "thumbnail": photos_data[0]['preview_path'] if photos_data else None,
            "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source_path": collection_source,
            "photos": photos_data
        }

        # Write the collection data to a JSON file
        json_file_path = os.path.join(new_collection_path, 'collection.json')
        self.write_json(collection_data, json_file_path)
        
    def write_json(self, data, file_path):
        """
        Write data to a JSON file.
        
        Args:
            data (dict): The data to write to the JSON file.
            file_path (str): The path where the JSON file will be saved.

        returns:
            str: The path to the written JSON file.
        """
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

        return file_path
    
    def read_json(self, file_path):
        """Read and return JSON data from a file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading JSON from {file_path}: {e}")
            return None


    def extract_jpg_from_raw(self, raw_file_path, output_path):
        """
        Extract JPG files from a RAW file.
        Args:
            raw_file_path (str): The path to the RAW file.
            output_path (str): The directory where the extracted JPG file will be saved.

        Returns:
            str: The path to the extracted JPG file, or None if no preview was found.
        """

        file_ext = os.path.splitext(raw_file_path)[1]
        file_name = f"{os.path.basename(raw_file_path)}{file_ext}"

        # If this file is a jpg, png, or jpeg, copy it to the output path and return the path to the copied file
        if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            ## Resize the image and save it using PhotoAnalyzer
            resized_image = PhotoAnalyzer.resize_image(cv.imread(raw_file_path), target_width=800)
            output_file_path = os.path.join(output_path, f"{os.path.splitext(file_name)[0]}_preview.jpg")
            cv.imwrite(output_file_path, resized_image)
            return output_file_path

        # Try to extract preview JPEG from RAW file
        try:
            with rawpy.imread(raw_file_path) as raw:
                thumb = raw.extract_thumb()
                if thumb.format == rawpy.ThumbFormat.JPEG:
                    ## Resize the thumbnail and save
                    thumb_image = cv.imdecode(np.frombuffer(thumb.data, np.uint8), cv.IMREAD_COLOR)
                    resized_image = PhotoAnalyzer.resize_image(thumb_image, target_width=800)
                    output_file_path = os.path.join(output_path, f"{os.path.splitext(file_name)[0]}_preview.jpg")
                    cv.imwrite(output_file_path, resized_image)
                    return output_file_path
                else:
                    print(f"No JPEG preview found in RAW file: {raw_file_path}")
                    return None
        except Exception as e:
            print(f"Error extracting preview from RAW file {raw_file_path}: {e}")
            return None
        

    ## ------ STATIC MEHTODS ------ ##
    @staticmethod
    def open_file_dialog(selection_type='file'):
        """
        Open a file dialog to select a file or directory, with the dialog appearing on top.

        Args:
            selection_type (str): Type of selection ('file' or 'directory').

        Returns:
            str: The selected file or directory path.
        """
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        if selection_type == 'file':
            file_path = filedialog.askopenfilename(parent=root)
        elif selection_type == 'directory':
            file_path = filedialog.askdirectory(parent=root)
        else:
            raise ValueError("Invalid selection type. Use 'file' or 'directory'.")
        root.destroy()
        return file_path
    
    @staticmethod
    def get_files(path, include_subdirs=False, file_types=None):
        """
        Get all files in a directory.
        
        Args:
            path (str): The directory path to search for files.
            include_subdirs (bool): Whether to include files from subdirectories.
            file_types (list): List of file extensions to filter by (e.g., ['.jpg', '.png']). If None, all files are included.

        Returns:
            list: A list of file paths that match the criteria.
        """
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
    
    