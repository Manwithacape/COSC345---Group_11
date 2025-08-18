## ------ IMPORTS ------ ##
import os
import sys
import cv2 as cv 
import numpy as np


class PhotoAnalyzer:
    """Class to handle photo analysis for the PhotoSIFT application."""

    def __init__(self, source_path, collection_path):
        self.source_path = source_path
        self.collection_path = collection_path
        self.resized_image_path = None  # Placeholder for resized image path


    def save_image(image, file_name, save_path):
        """Save an image to the specified path."""

        file_path = os.path.join(save_path, file_name)
        cv.imwrite(file_path, image)
        return file_path
    