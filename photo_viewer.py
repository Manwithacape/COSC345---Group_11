import ttkbootstrap as ttk
from PIL import Image, ImageTk
from main_viewer import MainViewer
from base_viewer import BaseThumbnailViewer

class PhotoViewer(BaseThumbnailViewer, MainViewer):
    """Scrollable grid of photo thumbnails with selection."""

    def __init__(self, parent, db, **kwargs):
        BaseThumbnailViewer.__init__(self, parent, db=db, thumb_size=120, padding=10, **kwargs)
        MainViewer.__init__(self, parent, **kwargs)

        self.selected_idx = None
        self.thumb_size = 120
        self.padding = 10
        self.columns = 1
        self.refresh_photos()

    def refresh_photos(self, collection_id=None):
        self.clear_thumbnails()
        self.photos = self.db.get_photos(collection_id)

        for photo in self.photos:
            tk_img = self.load_thumbnail(photo["file_path"])
            if not tk_img:
                continue
            self.thumbs.append(tk_img)
            lbl = ttk.Label(
                self.inner_frame,
                image=tk_img,
                cursor="hand2",
                bootstyle="dark",
                relief="flat"
            )
            lbl.image = tk_img
            lbl.photo_id = photo["id"]
            lbl.photo_path = photo["file_path"]
            lbl.bind("<Button-1>", lambda e, pid=photo["id"]: self._on_photo_click(pid))
            self.labels.append(lbl)

        self._reflow_grid()

        # Auto-select the first photo if any exist
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

    def _on_resize(self, event):
        """Reflow thumbnails on resize."""
        if not self.labels:
            return
        width = self.canvas.winfo_width()
        if width < 50:
            self.after(50, self._on_resize, event)
            return
        self.columns = max(1, width // (self.thumb_size + self.padding))
        self._reflow_grid()

    def _reflow_grid(self):
        if not self.labels:
            return
        for lbl in self.labels:
            lbl.grid_forget()
        for idx, lbl in enumerate(self.labels):
            row, col = divmod(idx, self.columns)
            lbl.grid(row=row, column=col, padx=5, pady=5, sticky="nw")
