# single_photo_viewer.py
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from main_viewer import MainViewer

class SinglePhotoViewer(MainViewer):
    """
    Show a single photo at 1:1 size inside the MainViewer canvas.
    The inner_frame matches the viewport; scrollbars appear if the image is larger.
    """

    def __init__(self, parent, photo_path=None, **kwargs):
        # Remove photo_path from kwargs before calling super
        kwargs.pop("photo_path", None)
        super().__init__(parent, **kwargs)

        self.photo_path = photo_path
        self.original_image = None
        self.tk_image = None

        # Image label inside inner_frame
        self.image_label = ttk.Label(self.inner_frame)
        self.image_label.pack(anchor="nw")

        # Set flag so MainViewer doesn’t try to reflow grid
        self.single_item_active = True

        # Load image if provided
        if photo_path:
            self.load_image(photo_path)

        # Make inner_frame always match canvas size
        self.canvas.bind("<Configure>", self._resize_inner_frame)

    def _resize_inner_frame(self, event=None):
        # The inner_frame will be at least as big as the image
        if self.original_image:
            width, height = self.original_image.size
        else:
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
        self.canvas.itemconfig(self.window_id, width=max(self.canvas.winfo_width(), width))
        self.canvas.itemconfig(self.window_id, height=max(self.canvas.winfo_height(), height))

    def load_image(self, photo_path):
        """Load the image at 1:1 size."""
        try:
            self.photo_path = photo_path
            self.original_image = Image.open(photo_path)
            self.tk_image = ImageTk.PhotoImage(self.original_image)
            self.image_label.config(image=self.tk_image)
            # Resize inner frame to match image immediately
            self._resize_inner_frame()
        except Exception as e:
            print(f"Failed to load image {photo_path}: {e}")
