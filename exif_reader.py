# exif_reader.py
from pathlib import Path
from PIL import Image
import piexif
import os
import rawpy
import exifread

class ExifReader:
    """
    Safely extract EXIF data from images.
    Handles bytes, rationals, nested tuples, None, and missing IFDs.
    """
    @staticmethod
    def read_exif(file_path: Path) -> dict:
        exif_data = {}

        raw_extensions = {'.cr2', '.nef', '.arw', '.dng', '.rw2', '.orf', '.raf', '.srw', '.pef'}
        ext = os.path.splitext(str(file_path))[1].lower()
        try:
            if ext in raw_extensions:
                # Use exifread for RAW files
                try:
                    with open(str(file_path), 'rb') as f:
                        tags = exifread.process_file(f, details=False)
                    for k, v in tags.items():
                        exif_data[str(k)] = str(v)
                except Exception as re:
                    print(f"Failed to read RAW EXIF from {file_path}: {re}")
            else:
                img = Image.open(file_path)
                raw_exif = img.info.get("exif")
                if not raw_exif:
                    return exif_data
                exif_dict = piexif.load(raw_exif)
                for ifd_name, ifd in exif_dict.items():
                    if not isinstance(ifd, dict):
                        continue
                    for tag, value in ifd.items():
                        tag_info = piexif.TAGS.get(ifd_name, {}).get(tag, {"name": str(tag)})
                        tag_name = tag_info["name"]
                        exif_data[tag_name] = ExifReader._normalize_value(value)
        except Exception as e:
            print(f"Failed to read EXIF from {file_path}: {e}")
        return exif_data

    @staticmethod
    def _normalize_value(value):
        """Convert EXIF values to Python-friendly types."""
        if value is None:
            return ""
        if isinstance(value, bytes):
            return value.decode("utf-8", errors="ignore").replace("\x00", "")
        if isinstance(value, tuple):
            if len(value) == 2 and all(isinstance(v, int) for v in value):
                num, den = value
                return num / den if den != 0 else None
            return tuple(ExifReader._normalize_value(v) for v in value)
        if isinstance(value, list):
            return [ExifReader._normalize_value(v) for v in value]
        return value