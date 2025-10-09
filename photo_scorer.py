# photo_scorer.py
import cv2
import numpy as np
from skimage import filters
from db import Database
import rawpy
from io import BytesIO


class PhotoScorer:
    """
    Comprehensive image scoring using OpenCV and skimage.
    Stores all computed metrics in the database if a DB instance is provided.
    """

    def __init__(self, db: Database = None):
        self.db = db

    def score_photo(self, file_path):
        """
        Compute a variety of metrics for the image.
        Returns a dictionary of metric_name -> value.
        If RAW, extract JPEG thumbnail and score that.
        """
        import os

        raw_extensions = {
            ".cr2",
            ".nef",
            ".arw",
            ".dng",
            ".rw2",
            ".orf",
            ".raf",
            ".srw",
            ".pef",
        }
        ext = os.path.splitext(file_path)[1].lower()
        img = None
        if ext in raw_extensions:
            try:
                with rawpy.imread(file_path) as raw:
                    thumb = raw.extract_thumb()
                    if thumb.format == rawpy.ThumbFormat.JPEG:
                        img_array = np.frombuffer(thumb.data, dtype=np.uint8)
                        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                    else:
                        img = thumb.data
            except Exception as re:
                print(f"Failed to extract RAW thumbnail for scoring: {file_path}: {re}")
        if img is None:
            img = cv2.imread(file_path)
        if img is None:
            raise ValueError(f"Cannot read image: {file_path}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        ## Resize to max dimension of 800 for faster processing | maintain aspect ratio
        max_dim = 800
        height, width = gray.shape
        if max(height, width) > max_dim:
            scale = max_dim / max(height, width)
            new_size = (int(width * scale), int(height * scale))
            gray = cv2.resize(gray, new_size, interpolation=cv2.INTER_AREA)
            hsv = cv2.resize(hsv, new_size, interpolation=cv2.INTER_AREA)
            img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)

        scores = {
            # ---------------- Sharpness / focus ----------------
            "laplacian_var": float(cv2.Laplacian(gray, cv2.CV_64F).var()),
            "sobel_energy": float(
                np.sum(np.square(cv2.Sobel(gray, cv2.CV_64F, 1, 0)))
                + np.sum(np.square(cv2.Sobel(gray, cv2.CV_64F, 0, 1)))
            ),
            # ---------------- Noise ----------------
            "noise": float(np.mean(np.abs(gray - cv2.GaussianBlur(gray, (3, 3), 0)))),
            # ---------------- Exposure / brightness ----------------
            "brightness_mean": float(np.mean(gray)),
            "brightness_median": float(np.median(gray)),
            "saturation_mean": float(np.mean(hsv[:, :, 1])),
            "saturation_std": float(np.std(hsv[:, :, 1])),
            # ---------------- Contrast ----------------
            "contrast_std": float(np.std(gray)),
            "contrast_range": float(gray.max() - gray.min()),
            # ---------------- Colorfulness ----------------
            "colorfulness": self._colorfulness(img),
            # ---------------- Entropy / texture ----------------
            "entropy": float(self._entropy(gray)),
            # ---------------- Size / aspect ----------------
            "width": img.shape[1],
            "height": img.shape[0],
            "aspect_ratio": img.shape[1] / img.shape[0],
        }

        return scores

    def scale_scores(self, scores):
        """
        Scale scores to a float between 0 (bad) and 1 (good) based on predefined min/max values.
        Returns a dictionary of metric_name -> scaled_value.
        """
        scaling_params = {
            "laplacian_var": (0, 1000),
            "sobel_energy": (0, 1e6),
            "noise": (0, 50),
            "brightness_mean": (0, 255),
            "brightness_median": (0, 255),
            "saturation_mean": (0, 255),
            "saturation_std": (0, 128),
            "contrast_std": (0, 128),
            "contrast_range": (0, 255),
            "colorfulness": (0, 100),
            "entropy": (0, 8),
            "width": (640, 8000),
            "height": (480, 6000),
            "aspect_ratio": (0.5, 2.0),
        }

        # Define which metrics are "higher is better" (good if high, bad if low)
        higher_is_better = {
            "laplacian_var",
            "sobel_energy",
            "brightness_mean",
            "brightness_median",
            "saturation_mean",
            "contrast_std",
            "contrast_range",
            "colorfulness",
            "entropy",
        }
        # Metrics where "lower is better" (good if low, bad if high)
        lower_is_better = {"noise", "saturation_std"}
        # For width, height, aspect_ratio, treat values near the middle of the range as best
        middle_is_better = {"width", "height", "aspect_ratio"}

        scaled_scores = {}
        for metric, value in scores.items():
            if metric in scaling_params:
                min_val, max_val = scaling_params[metric]
                if metric in higher_is_better:
                    # 1 is good (max), 0 is bad (min)
                    scaled = (value - min_val) / (max_val - min_val)
                elif metric in lower_is_better:
                    # 1 is good (min), 0 is bad (max)
                    scaled = 1.0 - ((value - min_val) / (max_val - min_val))
                elif metric in middle_is_better:
                    # Best is middle of range, worst is either extreme
                    mid_val = (min_val + max_val) / 2.0
                    dist = abs(value - mid_val) / ((max_val - min_val) / 2.0)
                    scaled = 1.0 - min(dist, 1.0)  # 1.0 at center, down to 0.0 at edges
                else:
                    scaled = 0.5  # Neutral if unknown
                # Clamp between 0 and 1
                scaled = max(0.0, min(1.0, float(scaled)))
                scaled_scores[metric] = scaled
            else:
                scaled_scores[metric] = float(value)  # No scaling applied

        return scaled_scores

    def score_and_store(self, photo_id, file_path):
        """
        Compute all metrics and store them in the DB for the given photo_id.
        """
        if self.db is None:
            raise ValueError("Database instance not provided.")
        scores = self.score_photo(file_path)
        scaled_scores = self.scale_scores(scores)
        # face_bboxes = self.detect_faces(file_path)

        # Save all unscaled metrics
        for metric_name, value in scores.items():
            self.db.add_score(
                photo_id, metric_name, float(value), scaled_scores[metric_name]
            )

        # Store detected face bounding boxes
        for bbox in face_bboxes:
            self.db.create_face(photo_id, bbox)

        # Compute and store overall quality score
        overall_quality = self.average_quality_score(photo_id, scaled_scores)
        return scores, scaled_scores

    def average_quality_score(self, photo_id, scaled_scores):
        """
        Compute an overall quality score as the average of selected scaled metrics.
        Store this overall quality score in a separate table.
        """
        if self.db is None:
            raise ValueError("Database instance not provided.")

        # Select metrics to include in overall quality score
        relevant_metrics = [
            "laplacian_var",
            "sobel_energy",
            "noise",
            "brightness_mean",
            "saturation_mean",
            "contrast_std",
            "colorfulness",
            "entropy",
        ]
        valid_scores = [
            scaled_scores[m] for m in relevant_metrics if m in scaled_scores
        ]
        if not valid_scores:
            overall_score = 0.0
        else:
            overall_score = float(
                np.mean(valid_scores)
            )  # FOR NOW A SIMPLE AVERAGE OF THE SCALED SCORES. LATER WEIGHT THEM

        # Store overall quality score
        self.db.add_quality_score(photo_id, overall_score)
        return overall_score

    # ---------------- Metric helpers ----------------
    def _colorfulness(self, img):
        """
        Measures colorfulness using the Hasler & Süsstrunk method.
        """
        (B, G, R) = cv2.split(img.astype("float"))
        rg = np.abs(R - G)
        yb = np.abs(0.5 * (R + G) - B)
        return float(
            np.sqrt(rg.mean() ** 2 + yb.mean() ** 2) + 0.3 * (rg.std() + yb.std())
        )

    def _entropy(self, gray):
        """
        Computes Shannon entropy of a grayscale image.
        """
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist_norm = hist.ravel() / hist.sum()
        hist_norm = hist_norm[hist_norm > 0]
        return float(-np.sum(hist_norm * np.log2(hist_norm)))

    # ------ FACE DETECTION ------
    def detect_faces(self, file_path):
        """
        Detect faces in the image using OpenCV's Haar cascades.
        Returns a list of bounding boxes [(x, y, w, h), ...].
        """
        # attempt to read the image
        cv_image = cv2.imread(file_path)
        if cv_image is None:
            raise ValueError(f"Cannot read image for face detection: {file_path}")

        # set up the face detector
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        # Convert to grayscale
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        # Convert to list of tuples (left, upper, right, lower)
        bounding_boxes = [self.convert_bbox(face) for face in faces]

        return bounding_boxes

    def convert_bbox(self, bbox):
        """
        Convert (x, y, w, h) to (left, upper, right, lower) as native Python ints.
        """
        x, y, w, h = bbox
        return (int(x), int(y), int(x + w), int(y + h))
