# photo_viewer.py
import ttkbootstrap as ttk
from main_viewer import MainViewer
from base_viewer import BaseThumbnailViewer
from single_photo_viewer import SinglePhotoViewer
from PIL import Image, ImageTk

class PhotoViewer(BaseThumbnailViewer, MainViewer):
    """Scrollable grid of photo thumbnails with single-photo preview support."""

    def __init__(self, parent, db, **kwargs):
        kwargs.pop("db", None)
        super().__init__(parent, **kwargs)
        BaseThumbnailViewer.__init__(self, parent, db=db, thumb_size=120, padding=10)

        self.thumb_size = 120
        self.padding = 10
        self.columns = 1
        self.labels = []
        self.thumbs = []
        self.single_item_active = False
        self.selected_idx = None
        self.db = db

        # NEW: a dedicated container we PACK, and GRID only inside here
        self.grid_area = ttk.Frame(self.inner_frame)
        self.grid_area.pack(fill="both", expand=True)

        self.refresh_photos()

    def refresh_photos(self, collection_id=None):
        """Load photos as thumbnails."""
        # Do NOT mix pack/grid parents: clear only our own label widgets
        for lbl in self.labels:
            try:
                lbl.destroy()
            except:
                pass
        self.labels = []
        self.thumbs = []

        # Leave single-photo mode if active
        if getattr(self, "single_photo_viewer", None):
            self.single_photo_viewer.destroy()
            self.single_photo_viewer = None
        self.single_item_active = False

        # Make sure grid_area is visible
        if not self.grid_area.winfo_ismapped():
            self.grid_area.pack(fill="both", expand=True)

        self.photos = self.db.get_photos(collection_id)

        for photo in self.photos:
            tk_img = self.load_thumbnail(photo["file_path"])
            if not tk_img:
                continue
            self.thumbs.append(tk_img)

            # IMPORTANT: parent is grid_area (not inner_frame)
            lbl = ttk.Label(
                self.grid_area,
                image=tk_img,
                cursor="hand2",
                bootstyle="dark",
                relief="flat"
            )
            lbl.image = tk_img
            lbl.photo_id = photo["id"]
            lbl.photo_path = photo["file_path"]

            # sanity check during dev; remove later if you like
            assert lbl.master is self.grid_area, f"Thumb parent is {lbl.master}, expected grid_area"

            lbl.bind("<Button-1>", lambda e, pid=photo["id"]: self._on_photo_click(pid))
            lbl.bind("<Double-1>", lambda e, path=photo["file_path"]: self._show_single_photo(path))

            self.labels.append(lbl)

        self._reflow_grid()

        # Auto-select first photo
        if self.labels:
            self._select_idx(0)
            self.select_photo(self.labels[0].photo_id)

    def _on_photo_click(self, photo_id):
        idx = next((i for i, lbl in enumerate(self.labels) if lbl.photo_id == photo_id), None)
        if idx is not None:
            self._select_idx(idx)
        self.select_photo(photo_id)

    def _select_idx(self, idx):
        if self.selected_idx is not None and 0 <= self.selected_idx < len(self.labels):
            self.labels[self.selected_idx].config(relief="flat")
        self.selected_idx = idx
        self.labels[idx].config(relief="solid")

    def _on_resize(self, event=None):
        if self.single_item_active or not self.labels:
            return
        width = self.canvas.winfo_width()
        if width < 50:
            self.after(50, self._on_resize, event)
            return
        self.columns = max(1, width // (self.thumb_size + self.padding))
        self._reflow_grid()

    def _reflow_grid(self):
        if not self.labels or self.single_item_active:
            return
        for lbl in self.labels:
            if lbl.winfo_exists():
                lbl.grid_forget()
        for idx, lbl in enumerate(self.labels):
            if lbl.winfo_exists():
                row, col = divmod(idx, self.columns)
                lbl.grid(row=row, column=col, padx=5, pady=5, sticky="nw")

    def _show_single_photo(self, photo_path):
        """Switch from thumbnail grid to single-photo view."""
        # Hide the grid (don't destroy the container)
        for lbl in self.labels:
            if lbl.winfo_exists():
                lbl.grid_forget()
        self.grid_area.pack_forget()

        # Remove old single-photo view if it exists
        if getattr(self, "single_photo_viewer", None):
            self.single_photo_viewer.destroy()

        self.single_item_active = True
        self.single_photo_viewer = SinglePhotoViewer(self.inner_frame, photo_path)
        self.single_photo_viewer.pack(fill="both", expand=True)
