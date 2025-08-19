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

    @staticmethod
    def save_image(image, file_name, save_path):
        """Save an image to the specified path."""

        file_path = os.path.join(save_path, file_name)
        cv.imwrite(file_path, image)
        return file_path
    
    @staticmethod
    def resize_image(image, target_width, maintain_aspect_ratio=True):
        """
        Resize an image to the target size.

        Args:
            image_path (str): Path to the image file.
            target_size (tuple): Target size as (width, height).
            maintain_aspect_ratio (bool): Whether to maintain aspect ratio.

        Returns:
            str: Path to the resized image.
        """
        if maintain_aspect_ratio:
            height, width = image.shape[:2]
            aspect_ratio = width / height
            target_height = int(target_width / aspect_ratio)
            resized_image = cv.resize(image, (target_width, target_height))
        else:
            resized_image = cv.resize(image, (target_width, target_width))

        return resized_image
    

    