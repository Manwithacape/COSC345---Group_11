"""Base thumbnail viewer: loads images (incl. common RAWs), builds thumbnails,
tracks selection, and notifies linked viewers (EXIF/score/filmstrip/faces)."""

# stdlib first
import os
from io import BytesIO

# third-party
import ttkbootstrap as ttk
from PIL import Image, ImageTk
import rawpy

# --- Compatibility shims (minimal) -------------------------------------------

# Pillow resampling compatibility (avoid E1101 and always define a value)
try:
    RESAMPLE_LANCZOS = Image.Resampling.LANCZOS  # type: ignore[attr-defined]
except (NameError, AttributeError):
    # Fall back to LANCZOS or BICUBIC; final fallback uses 0 (NEAREST).
    RESAMPLE_LANCZOS = getattr(Image, "LANCZOS", getattr(Image, "BICUBIC", 0))

# rawpy exception compatibility (avoid E1101 on some builds)
try:
    RawpyLibRawError = rawpy.LibRawError  # type: ignore[attr-defined]
except AttributeError:
    class RawpyLibRawError(Exception):
        """Fallback when rawpy.LibRawError is unavailable."""
        # no pass needed; docstring provides the body
        ...

class BaseThumbnailViewer(  # pylint: disable=too-many-ancestors
    ttk.Frame
):
    """
    Shared base class for displaying photo thumbnails.
    Handles loading images, keeping references, selection,
    and notifying parent/other viewers.
    """

    def __init__(self, parent, db=None, thumb_size=100, padding=5, **kwargs):
        super().__init__(parent, **kwargs)
        self.db = db
        self.thumb_size = thumb_size
        self.padding = padding
        self.labels = []  # Tk Labels for thumbnails
        self.thumbs = []  # ImageTk.PhotoImage refs
        self.photos = []  # DB rows or metadata dicts
        self.selected_id = None

    def _open_image(self, file_path):
        """Open an image path and return a PIL Image. Handles common RAWs via rawpy."""
        raw_extensions = {
            ".cr2", ".nef", ".arw", ".dng", ".rw2",
            ".orf", ".raf", ".srw", ".pef",
        }
        ext = os.path.splitext(file_path)[1].lower()
        if ext in raw_extensions:
            with rawpy.imread(file_path) as raw:
                thumb = raw.extract_thumb()
                # Avoid direct enum reference to silence E1101 on some rawpy versions
                is_jpeg = getattr(getattr(thumb, "format", None), "name", None) == "JPEG"
                if is_jpeg:
                    return Image.open(BytesIO(thumb.data))
                return Image.fromarray(thumb.data)
        return Image.open(file_path)

    def create_uniform_thumbnail_pil(self, file_path, bg_color=(30, 30, 30)):
        """
        Create a square, letterboxed thumbnail as a PIL.Image with side = self.thumb_size.
        Preserves aspect ratio (no stretching) and centers on a background.
        Returns None on error.
        """
        try:
            img = self._open_image(file_path)
            # Ensure RGB (avoid issues with palette/LA modes)
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")

            # Scale to fit within the square
            size = int(self.thumb_size)
            img_copy = img.copy()
            img_copy.thumbnail((size, size), RESAMPLE_LANCZOS)

            # Create square canvas and paste centered
            canvas = Image.new("RGB", (size, size), color=bg_color)
            x = (size - img_copy.width) // 2
            y = (size - img_copy.height) // 2
            if img_copy.mode == "RGBA":
                canvas.paste(img_copy, (x, y), mask=img_copy.split()[-1])
            else:
                canvas.paste(img_copy, (x, y))
            return canvas
        except (OSError, RawpyLibRawError, ValueError) as exc:
            # OSError covers PIL IO/decoding.
            # RawpyLibRawError covers RAW decoding issues; ValueError for malformed data.
            print(f"Failed to create uniform thumbnail for {file_path}: {exc}")
            return None

    def load_thumbnail(self, file_path):
        """Return ImageTk.PhotoImage uniform square thumbnail for display (or None on error)."""
        try:
            pil_thumb = self.create_uniform_thumbnail_pil(file_path)
            if pil_thumb is None:
                return None
            return ImageTk.PhotoImage(pil_thumb)
        except (OSError, ValueError) as exc:
            print(f"Failed to load thumbnail for {file_path}: {exc}")
            return None

    def clear_thumbnails(self):
        """Destroy all thumbnail labels and clear image references."""
        for lbl in self.labels:
            lbl.destroy()
        self.labels = []
        self.thumbs = []

    def select_photo(self, photo_id):
        """Highlight a selected thumbnail and update linked viewers."""
        self.selected_id = photo_id
        for lbl in self.labels:
            if getattr(lbl, "photo_id", None) == photo_id:
                lbl.config(relief="solid")
            else:
                lbl.config(relief="flat")

        # Notify parent container if available
        self._notify(photo_id)

    def _notify(self, photo_id):
        """Call updates on linked viewers if parent has them."""
        master = self.master
        # Filmstrip, EXIF, score, duplicate, and faces viewers may exist in parent
        if hasattr(master, "exif_viewer") and master.exif_viewer:
            master.exif_viewer.update_content(photo_id)
        if hasattr(master, "score_viewer") and master.score_viewer:
            master.score_viewer.update_content(photo_id)
        if hasattr(master, "filmstrip") and master.filmstrip:
            master.filmstrip.update_highlight(photo_id)
        if hasattr(master, "duplicate_viewer") and master.duplicate_viewer:
            master.duplicate_viewer.update_content(photo_id)
        if hasattr(master, "faces_viewer") and master.faces_viewer:
            master.faces_viewer.update_faces(photo_id)
