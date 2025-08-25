## ------ IMPORTS ------ ##
import os
import sys
import cv2 as cv 
import numpy as np
from PIL import Image
from sentence_transformers import SentenceTransformer, util

class PhotoAnalyzer:
    @staticmethod
    def resize_image(image, target_width=800):
        """Resize image to target width, maintaining aspect ratio."""
        if image is None:
            return None
        h, w = image.shape[:2]
        if w == 0:
            return image
        scale = target_width / w
        new_size = (int(w * scale), int(h * scale))
        return cv.resize(image, new_size, interpolation=cv.INTER_AREA)

    @staticmethod
    def load_image(image_path):
        """Load an image from the specified path."""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        return cv.imread(image_path)
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
        gray_image = PhotoAnalyzer.grayscale(image)
        laplacian_var = cv.Laplacian(gray_image, cv.CV_64F).var()
        # Normalize the variance to a range of 0 to 1
        sharpness = PhotoAnalyzer.map_value(laplacian_var, 0, 1000, 0, 1)
        return sharpness

    @staticmethod
    def exposure_value(image):
        """
        Detect the exposure of an image as a proportion:
        1 = well-exposed (not too dark or too bright),
        0 = underexposed or overexposed.
        """
        gray_image = PhotoAnalyzer.grayscale(image)
        mean_intensity = np.mean(gray_image)
        # Assume ideal exposure is around mid-gray (127.5)
        # The further from 127.5, the worse the exposure
        exposure = 1.0 - (abs(mean_intensity - 127.5) / 127.5)
        exposure = max(0.0, min(1.0, exposure)) 
        return exposure
    
    @staticmethod
    def contrast_value(image):
        """
        Detect the contrast of an image as a proportion:
        1 = high contrast, 0 = low contrast.
        """
        gray_image = PhotoAnalyzer.grayscale(image)
        min_val = np.min(gray_image)
        max_val = np.max(gray_image)
        contrast = (max_val - min_val) / 255.0
        return contrast
    
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
    def score_image(image_path, sharpness_weight=1, exposure_weight=1, saturation_weight=1, contrast_weight=1):
        """
        returns a tuple with sharpness, exposure, saturation, contrast, and overall score (for now assuming weights of 1).
        """
        image = PhotoAnalyzer.load_image(image_path);

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
    def weighted_average(values, weights):
        """Calculate a weighted average of the given values."""
        if len(values) != len(weights):
            raise ValueError("Values and weights must have the same length.")
        total = 0
        for i in range(len(values)):
            total += values[i] * weights[i]
        
        return total / len(values);

    @staticmethod
    def find_duplicates(image_paths, threshold=0.99, top_k=10, model_name="clip-ViT-B-32"):
        """
        Group images into duplicate/near duplicate clusters using CLIP embeddings.

        :param image_paths (list[str]): List of image file paths
        :param threshold (float): Cosine similarity threshold (1.0 = exact duplicates)
        :top_k (int): Number of top duplicate/near-duplicate pairs to return - if show all set top_k=None
        :param model name(str): CLIP model to use

        :return dict{"duplicates": [...], "near-duplicates": [...]}: Each a list of tuples (score, path1, path2)
        """

        print("Loading CLIP Model...")
        model = SentenceTransformer(model_name)

        print(f"Encoding {len(image_paths)} images...")
        encoded = model.encode(
            [Image.open(fp).convert("RGB") for fp in image_paths], batch_size=32,
            convert_to_tensor=False, show_progress_bar=True
        )

        print("Computing similarities..")
        processed = util.paraphrase_mining_embeddings(encoded)

        # Duplicates: exact matches
        duplicates = [
            (score, image_paths[i1], image_paths[i2])
            for score, i1, i2 in processed if score >= 0.999
        ][:top_k]

        # Near-duplicates: Above threshold but not exact
        near_duplicates = [
            (score, image_paths[i1], image_paths[i2])
            for score, i1, i2 in processed if threshold <= score < 0.999
        ][:top_k]

        print("Computation complete!")

        return{
            "duplicates": duplicates,
            "near_duplicates": near_duplicates
        }