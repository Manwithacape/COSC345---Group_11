# single_photo_viewer.py
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from main_viewer import MainViewer

class SinglePhotoViewer(MainViewer):
    """
    Shows one photo scaled-to-fit and centered directly on the Canvas.
    """

    def __init__(self, parent, photo_path=None, **kwargs):
        kwargs.pop("photo_path", None)
        super().__init__(parent, **kwargs)

        # enter single-photo mode
        self.single_item_active = True

        # hide the grid layer and scrollbar in single view
        try:
            self.canvas.itemconfigure(self.window_id, state="hidden")
        except Exception:
            pass
        try:
            self.scrollbar_y.pack_forget()
        except Exception:
            pass

        self.canvas.configure(highlightthickness=0, bg="#222")

        # image state
        self.photo_path = None
        self._orig_img = None
        self._img_tk = None
        self._img_item = None

        # redraw when the canvas resizes
        self.canvas.bind("<Configure>", self._on_resize)

        if photo_path:
            self.load_image(photo_path)

    def load_image(self, photo_path: str):
        """Load the image and render to fit canvas."""
        try:
            self.photo_path = photo_path
            self._orig_img = Image.open(photo_path).convert("RGBA")
            self._render_fit()
        except Exception as e:
            print(f"[SinglePhotoViewer] Failed to load {photo_path}: {e}")

    def _on_resize(self, _event=None):
        if self._orig_img is not None:
            self._render_fit()

    def _render_fit(self):
        """Scale image to fit canvas while preserving aspect ratio and center it."""
        cw = max(1, self.canvas.winfo_width())
        ch = max(1, self.canvas.winfo_height())
        iw, ih = self._orig_img.size
 
        scale = min(cw / iw, ch / ih)
        new_w = max(1, int(iw * scale))
        new_h = max(1, int(ih * scale))
 
        img_resized = self._orig_img.resize((new_w, new_h), Image.LANCZOS)
        self._img_tk = ImageTk.PhotoImage(img_resized)
        self._img_tk = ImageTk.PhotoImage(img_resized)

        if self._img_item is not None:
            self.canvas.delete(self._img_item)

        cx, cy = cw // 2, ch // 2
        self._img_item = self.canvas.create_image(cx, cy, image=self._img_tk, anchor="center")
        self.canvas.tag_raise(self._img_item)

        # no scrolling in fit view
        self.canvas.config(scrollregion=(0, 0, cw, ch))

    # Optional: if you need to restore grid mode later
    def restore_grid_layer(self):
        self.single_item_active = False
        try:
            self.canvas.itemconfigure(self.window_id, state="normal")
        except Exception:
            pass
