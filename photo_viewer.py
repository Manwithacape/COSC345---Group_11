# photo_viewer.py
import ttkbootstrap as ttk
from main_viewer import MainViewer
from base_viewer import BaseThumbnailViewer
from PIL import Image, ImageTk, ImageDraw, ImageFont
from photo_analyzer import PhotoAnalyzer

class PhotoViewer(BaseThumbnailViewer, MainViewer):
    """Scrollable grid of photo thumbnails with single-photo preview support."""

    def __init__(self, parent, db, open_single_callback=None, **kwargs):
        kwargs.pop("db", None)
        super().__init__(parent, **kwargs)
        BaseThumbnailViewer.__init__(self, parent, db=db, thumb_size=120, padding=10)

        self.open_single_callback = open_single_callback  # <-- callback to app

        self.thumb_size = 120
        self.padding = 10
        self.columns = 1
        self.labels = []
        self.thumbs = []
        self.single_item_active = False
        self.selected_idx = None
        self.db = db
        self.photo_analyzer = PhotoAnalyzer(db)

        # dedicated container for the grid
        self.grid_area = ttk.Frame(self.inner_frame)
        self.grid_area.pack(fill="both", expand=True)

        self.refresh_photos()

    def add_score_overlay(self, image, rank, score):
        try:
            score = float(score)
        except Exception:
            score = 0.0
            
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        text_rank = f"#{rank}"
        draw.rectangle([0, 0, 60, 30], fill="black")
        draw.text((5, 5), text_rank, fill="white", font=font)

        text_score = f"{score:.2f}"
        draw.text((5, 15), text_score, fill="white", font=font)
        
        return image

    def refresh_photos(self, collection_id=None):
        """Load photos as thumbnails."""
        for lbl in self.labels:
            try:
                lbl.destroy()
            except:
                pass
        self.labels = []
        self.thumbs = []

        self.single_item_active = False

        # Make sure grid_area is visible
        if not self.grid_area.winfo_ismapped():
            self.grid_area.pack(fill="both", expand=True)

        self.photos = self.db.get_photos(collection_id)

        # Compute ranking
        ranked = self.photo_analyzer.rank_by_quality([p["id"] for p in self.photos])

        rank_map = {pid: idx + 1 for idx, (pid, _) in enumerate(ranked)}

        for photo in self.photos:
            tk_img = self.load_thumbnail(photo["file_path"])
            if not tk_img:
                continue

            score = self.db.get_quality_score(photo["id"])
            rank = rank_map.get(photo["id"], "-")

            if score is not None:
                pil_img = Image.open(photo["file_path"]).resize((self.thumb_size, self.thumb_size))
                pil_img = self.add_score_overlay(pil_img, rank, score)
                tk_img = ImageTk.PhotoImage(pil_img)

            self.thumbs.append(tk_img)

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

            lbl.bind("<Button-1>", lambda e, pid=photo["id"]: self._on_photo_click(pid))
            lbl.bind("<Double-1>", lambda e, path=photo["file_path"]: self._show_single_photo(path))

            self.labels.append(lbl)

        self._reflow_grid()

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
        """Ask the app to switch the center pane to a full SinglePhotoViewer."""
        if callable(self.open_single_callback):
            self.open_single_callback(photo_path)
