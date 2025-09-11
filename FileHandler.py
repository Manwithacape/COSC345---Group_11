"""
FileHandler.py
==============
PhotoSIFT File Handler

This module provides the FileHandler class for managing file operations,
database interactions, and image processing for the PhotoSIFT application.

Main features:
- Collection creation and management
- Thumbnail extraction and image analysis
- Integration with database and PhotoAnalyzer

Author: Group 11
"""
import os
import tkinter as tk
import json
import rawpy  # Ensure you have rawpy installed for RAW file handling
import cv2 as cv
import numpy as np
from tkinter import filedialog
from datetime import datetime
from PhotoAnalysis import PhotoAnalyzer  # Import the PhotoAnalyzer class
from db import Database  # Import the Database class

class FileHandler:
    """Class to handle file operations for the PhotoSIFT application."""
    def __init__(self):
        self.root_dir = os.path.expanduser('~')
        self.photoSIFT_dir = self.create_directory(os.path.join(self.root_dir, 'PhotoSIFT'))
        self.Collections_dir = self.create_directory(os.path.join(self.photoSIFT_dir, 'Collections'))
        self.db = Database();
    
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
    
    def get_all_collections(self, user_id=1):

        ## Get all collections from the database
        users_collection_rows = self.db.execute_query("SELECT * FROM collections where user_id = %s", (1,))  # Assuming user_id=1 for now

        ## pack them into a list of dicts
        users_collections = []
        for row in users_collection_rows:
            users_collections.append({
                'collection_id': row['collection_id'],
                'name': row['name'],
                'description': row['description'],
                'source_path': row['source_path'],
                'date_created': row['date_created'],
                'thumbnail_path': row['thumbnail_path']
            })
        return users_collections
    
    def create_collection(self, user_id, collection_name, colletion_description, collection_source):
        """
        Create a new photo collection by gathering photos from the specified source,
        extracting thumbnails, analyzing them, and storing the data in a JSON file and database.

        Args:
            collection_name (str): The name of the collection.
            colletion_description (str): A description of the collection.
            collection_source (str): The source path for the collection.
        """
        #Gather photo files
        photo_files = self.get_files(collection_source, include_subdirs=True)
        
        # Create a new collection directory
        collection_path = self.create_directory(os.path.join(self.Collections_dir, collection_name))

        # Extract and resize thumbnails
        photos_data = []
        for photo_path in photo_files:

            ## Get the thumbnail path
            thumbnail_path = self.get_and_save_thumbnail(photo_path, collection_path)

            ## Run image analysis on the thumbnail (returns a dict of scores)
            photo_scores = PhotoAnalyzer.score_image(thumbnail_path)

            ## Build photo data dict
            photo_data = {
                "original_path": photo_path,
                "thumbnail_path": thumbnail_path,
                "scores": {
                    "sharpness": photo_scores[0],
                    "exposure": photo_scores[1],
                    "saturation": photo_scores[2],
                    "contrast": photo_scores[3],
                    "weighted_score": photo_scores[4]
                }
            }

            ## Append to photos data list
            photos_data.append(photo_data)

        
        # Find or generate the collection thumbnail (e.g., first photo's thumbnail)
        collection_thumbnail_path = None
        if photos_data:
            collection_thumbnail_path = photos_data[0]["thumbnail_path"]

        # Insert the collection and get its ID
        collection_result = self.db.execute_query(
            "INSERT INTO collections (user_id, name, description, source_path, date_created, thumbnail_path) VALUES (%s, %s, %s, %s, %s, %s) RETURNING collection_id",
            (user_id, collection_name, colletion_description, collection_source, datetime.now(), collection_thumbnail_path)
        )
        if collection_result and isinstance(collection_result, list) and len(collection_result) > 0:
            collection_record_id = collection_result[0]['collection_id']
        else:
            print("Failed to insert collection into database.")
            return

        # Add each photo and its scores to the DB
        for photo in photos_data:
            # Insert photo and get its photo_id
            photo_result = self.db.execute_query(
                "INSERT INTO photos (collection_id, original_path, thumbnail_path) VALUES (%s, %s, %s) RETURNING photo_id",
                (collection_record_id, photo['original_path'], photo['thumbnail_path'])
            )
            if photo_result and isinstance(photo_result, list) and len(photo_result) > 0:
                photo_record_id = photo_result[0]['photo_id']
            else:
                print(f"Failed to insert photo: {photo['original_path']}")
                continue

            # Insert scores for this photo
            for metric_name, value in photo['scores'].items():
                # Convert NumPy types to native Python types
                if hasattr(value, 'item'):
                    value = value.item()
                self.db.execute_query(
                    "INSERT INTO scores (photo_id, metric_name, value) VALUES (%s, %s, %s) ON CONFLICT (photo_id, metric_name) DO UPDATE SET value = EXCLUDED.value",
                    (photo_record_id, metric_name, value)
                )
                ## Pack up the collection data and write to JSON
                collection_data = {
                    "name": collection_name,
                    "description": colletion_description,
                    "thumbnail": photos_data[0]['thumbnail_path'] if photos_data else None,
                    "created_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "source_path": collection_source,
                    "photos": photos_data
                }
                json_file_path = os.path.join(collection_path, 'collection.json')
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

    def get_and_save_thumbnail(self, image_path, output_path):
        ## Read the image using OpenCV
        image_extention = os.path.splitext(image_path)[1].lower()
        image_name = os.path.basename(image_path)

        ## if the image is not a jpg, jpeg, or png extract the
        if image_extention not in ['.jpg', '.jpeg', '.png']:
            image = self.extract_preview_from_raw(image_path)

        if image_extention in ['.jpg', '.jpeg', '.png']:
            image = cv.imread(image_path)
            if image is None:
                print(f"Error loading image {image_path}")
                return None
            
        ## Resize the image and save it using PhotoAnalyzer
        resized_image = PhotoAnalyzer.resize_image(image, target_width=800)
        thumbnail_path = os.path.join(output_path, f"thumb_{image_name}.jpg")
        cv.imwrite(thumbnail_path, resized_image)
        return thumbnail_path
    
    def extract_preview_from_raw(self, raw_file_path):
        """
        Extract a preview image and return it as a cv2 image object.
        
        Args:
            raw_file_path (str): The path to the RAW image file.
        """
        try:
            with rawpy.imread(raw_file_path) as raw:
                preview = raw.extract_thumb()
                if preview.format == rawpy.ThumbFormat.JPEG:
                    # Decode JPEG bytes to cv2 image
                    image = cv.imdecode(np.frombuffer(preview.data, np.uint8), cv.IMREAD_COLOR)
                    return image
                elif preview.format == rawpy.ThumbFormat.BITMAP:
                    # Convert bitmap to cv2 image
                    image = cv.cvtColor(preview.data, cv.COLOR_RGB2BGR)
                    return image
                else:
                    print(f"Unsupported thumbnail format in {raw_file_path}")
                    return None
        except Exception as e:
            print(f"Error extracting preview from {raw_file_path}: {e}")
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
    
    