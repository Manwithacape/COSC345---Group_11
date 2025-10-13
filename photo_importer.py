# photo_importer.py

from pathlib import Path
from db import Database
from duplicates import NearDuplicateDetector
from photo_scorer import PhotoScorer
from exif_reader import ExifReader
from photo_analyzer import PhotoAnalyzer

class PhotoImporter:
    """
    Class for importing photos into the database.
    """

    # Tuple of supported file extensions for photos
    SUPPORTED_EXTENSIONS = (
        ".jpg",
        ".jpeg",
        ".tif",
        ".tiff",
        ".cr2",
        ".nef",
        ".arw",
        ".dng",
        ".rw2",
        ".orf",
        ".raf",
        ".srw",
        ".pef",
    )

    def __init__(self, db: Database, near_dup_threshold=5):
        """
        Initialize the PhotoImporter with a database connection and other components.

        Args:
            db (Database): The database instance to interact with.
            near_dup_threshold (int): Threshold for near-duplicate detection.
        """
        self.db = db
        # Initialize NearDuplicateDetector with the provided threshold
        self.duplicates = NearDuplicateDetector(db, threshold=near_dup_threshold)
        # Initialize PhotoScorer to score photos
        self.scorer = PhotoScorer(db)
        # Initialize PhotoAnalyzer for analyzing photos
        self.photo_analyzer = PhotoAnalyzer(db)

    def import_files(self, file_paths: list[str], collection_id: int, default_styles=None):
        """
        Import a list of photo files into the database.

        Args:
            file_paths (list[str]): List of file paths to import.
            collection_id (int): The ID of the collection to which photos will be added.
            default_styles (list[str], optional): Default styles to assign to imported photos.

        Returns:
            int: Number of successfully imported photos.
        """
        imported_count = 0
        for file_path in file_paths:
            try:
                # Import each file and count successful imports
                self._import_file(Path(file_path), collection_id, default_styles)
                imported_count += 1
            except Exception as e:
                print(f"Skipping {file_path}: {e}")
        print(f"Imported {imported_count} photos")
        return imported_count

    def import_folder(self, folder_path: str, collection_id: int, default_styles=None):
        """
        Import all supported photo files from a specified folder.

        Args:
            folder_path (str): Path to the folder containing photos.
            collection_id (int): The ID of the collection to which photos will be added.
            default_styles (list[str], optional): Default styles to assign to imported photos.

        Returns:
            int: Number of successfully imported photos from the folder.
        """
        folder = Path(folder_path)
        # Check if the provided path is a valid directory
        if not folder.exists() or not folder.is_dir():
            raise ValueError(
                f"Folder {folder_path} does not exist or is not a directory"
            )

        # Collect all supported photo files from the folder
        files = [
            str(f)
            for f in folder.glob("*")
            if f.suffix.lower() in self.SUPPORTED_EXTENSIONS
        ]
        # Import the collected files
        return self.import_files(files, collection_id, default_styles)

    def _import_file(self, file: Path, collection_id: int, default_styles=None):
        """
        Internal method to import a single photo file.

        Args:
            file (Path): The path of the photo file to import.
            collection_id (int): The ID of the collection to which the photo will be added.
            default_styles (list[str], optional): Default styles to assign to the imported photo.

        Returns:
            int: The ID of the imported photo in the database.
        """
        # Check if the file has a supported extension
        if file.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {file.suffix}")

        # --- Extract EXIF using the dedicated reader ---
        exif = ExifReader.read_exif(file)

        # Add photo to database and get its ID
        photo_id = self.db.add_photo(
            collection_id=collection_id, file_path=str(file), file_name=file.name
        )

        # Automatically analyze new photo
        self.photo_analyzer.analyze_photo(photo_id, file_path=str(file))

        # Store EXIF data in the database
        for key, value in exif.items():
            self.db.add_exif(photo_id, key, str(value))

        # Assign default styles to the imported photo
        if default_styles:
            for style_name in default_styles:
                style_id = self.db.add_style(style_name)
                if style_id:
                    self.db.assign_style(photo_id, style_id)

        # Score the image and store scores in the database
        try:
            scores = self.scorer.score_and_store(photo_id, str(file))
            print(f"Scores for {file.name}: {scores}")
        except Exception as e:
            print(f"Failed to score {file.name}: {e}")

        print(f"Imported {file}")
        return photo_id
