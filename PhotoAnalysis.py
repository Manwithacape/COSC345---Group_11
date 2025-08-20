## ------ IMPORTS ------ ##
import os
import sys
import cv2 as cv 
import numpy as np


class PhotoAnalyzer:
    """Class to handle photo analysis operations."""
    @staticmethod
    def map_value(value, from_min, from_max, to_min, to_max):
        """Map a value from one range to another."""
        return (value - from_min) / (from_max - from_min) * (to_max - to_min) + to_min
    
    @staticmethod
    def grayscale(image):
        """Convert an image to grayscale."""
        return cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    
    @staticmethod
    def sharpness_value(image):
        """
        Calculate the sharpness of an image as a proportion:
        0 = blurry, 1 = sharp.
        """
        gray_image = PhotoAnalyzer.gray_image(image)
        laplacian_var = cv.Laplacian(gray_image, cv.CV_64F).var()
        # Normalize the variance to a range of 0 to 1
        sharpness = PhotoAnalyzer.map_value(laplacian_var, 0, 1000, 0, 1)

    @staticmethod
    def exposure_value(image):
        """
        Detect the exposure of an image as a proportion:
        1 = well-exposed (not too dark or too bright),
        0 = underexposed or overexposed.
        """
        gray_image = gray_image(image)
        mean_intensity = np.mean(gray_image)
        # Assume ideal exposure is around mid-gray (127.5)
        # The further from 127.5, the worse the exposure
        exposure = 1.0 - (abs(mean_intensity - 127.5) / 127.5)
        exposure = max(0.0, min(1.0, exposure)) 
        return exposure
    
    @staticmethod
    def saturation_value(image):
        """Detect the saturation of an image as a proportion: 0 (grayscale), 1 (fully saturated)."""
        hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        saturation_channel = hsv_image[:, :, 1]
        mean_saturation = np.mean(saturation_channel)
        # Normalize mean saturation (0 = grayscale, 255 = fully saturated)
        saturation = mean_saturation / 255.0
        saturation = max(0.0, min(1.0, saturation)) 
        return saturation
    
    @staticmethod 
    def score_image(image, sharpness_weight=1, exposure_weight=1, saturation_weight=1, contrast_weight=1):
        """
        returns a weighted average score for an image based on sharpness, exposure, saturation, and contrast.
        """
        if image is None:
            raise ValueError("Image cannot be None.")

        sharpness = PhotoAnalyzer.sharpness_value(image)
        exposure = PhotoAnalyzer.exposure_value(image)
        saturation = PhotoAnalyzer.saturation_value(image)
        contrast = PhotoAnalyzer.contrast_value(image)
        
        
        # Calculate the final score
        overall_score = PhotoAnalyzer.weighted_average(
            [sharpness, exposure, saturation, contrast],
            [sharpness_weight, exposure_weight, saturation_weight, contrast_weight]
        )
        
        return sharpness, exposure, saturation, contrast, overall_score
    
    @staticmethod
    def weighted_average(self, values, weights):
        """Calculate a weighted average of the given values."""
        if len(values) != len(weights):
            raise ValueError("Values and weights must have the same length.")
        return sum(v * w for v, w in zip(values, weights)) / sum(weights)