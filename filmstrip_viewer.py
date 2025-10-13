# filmstrip_viewer.py

import ttkbootstrap as ttk
from base_viewer import BaseThumbnailViewer

HIGHLIGHT_BORDER = 3

class FilmstripViewer(BaseThumbnailViewer):
    """
    Horizontal scrolling strip of thumbnails.
    Works with the new MainViewer-based PhotoViewer.
    """

    def __init__(
        self,
        parent,
        photo_viewer,
        exif_viewer=None,
        score_viewer=None,
        duplicates_viewer=None,
        **kwargs
    ):
        """
        Initialize FilmstripViewer.

        Args:
            parent: Parent widget for the filmstrip.
            photo_viewer: Main PhotoViewer instance to sync with.
            exif_viewer (optional): EXIF Viewer instance to display metadata.
            score_viewer (optional): Score Viewer instance to display ratings.
            duplicates_viewer (optional): Duplicates Viewer instance.
            **kwargs: Additional arguments for the BaseThumbnailViewer.
        """
        super().__init__(parent, thumb_size=80, padding=5, **kwargs)
        self.photo_viewer = photo_viewer
        self.exif_viewer = exif_viewer
        self.score_viewer = score_viewer
        self.duplicates_viewer = duplicates_viewer

        # Use MainViewer-style canvas
        self.canvas = ttk.Canvas(
            self, height=self.thumb_size + 2 * self.padding, highlightthickness=0
        )
        self.scrollbar = ttk.Scrollbar(
            self, orient="horizontal", command=self.canvas.xview
        )
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="bottom", fill="x")
        self.canvas.pack(side="top", fill="x", expand=True)

        self.inner_frame = ttk.Frame(self.canvas)
        self.window_id = self.canvas.create_window(
            (0, 0), window=self.inner_frame, anchor="nw"
        )
        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.refresh_thumbs()

    def refresh_thumbs(self):
        """
        Rebuild filmstrip from current photo viewer thumbnails.
        Clears existing thumbnails and loads new ones from the photo viewer.
        """
        self.clear_thumbnails()
        for lbl in getattr(self.photo_viewer, "labels", []):
            img_path = getattr(lbl, "photo_path", None)
            photo_id = getattr(lbl, "photo_id", None)
            if not img_path or not photo_id:
                continue

            tk_img = self.load_thumbnail(img_path)
            if not tk_img:
                continue

            self.thumbs.append(tk_img)

            thumb_lbl = ttk.Label(
                self.inner_frame,
                image=tk_img,
                cursor="hand2",
                bootstyle="dark",
                relief="solid",
            )
            thumb_lbl.image = tk_img
            thumb_lbl.photo_id = photo_id  # keep id on widget
            thumb_lbl.photo_path = img_path  # keep path too
            thumb_lbl.bind(
                "<Button-1>", lambda e, pid=photo_id: self.on_thumb_click(pid)
            )
            thumb_lbl.pack(side="left", padx=self.padding, pady=self.padding)
            self.labels.append(thumb_lbl)

        self.update_highlight()

    def update_highlight(self, selected_photo_id=None):
        """
        Update the highlight on the currently selected thumbnail.

        Args:
            selected_photo_id (optional): Photo ID of the newly selected thumbnail.
                                        If not provided, uses the last selected ID.
        """
        if selected_photo_id:
            self.selected_id = selected_photo_id
        for lbl in self.labels:
            if lbl.photo_id == getattr(self, "selected_id", None):
                lbl.config(relief="solid")
                self._scroll_to_label(lbl)
            else:
                lbl.config(relief="flat")

    def on_thumb_click(self, photo_id):
        """
        Handle click event on a thumbnail.
        Highlight the selected thumbnail, update the photo viewer grid,
        and show the single photo.

        Args:
            photo_id: ID of the clicked photo.
        """
        self.select_photo(photo_id)

        # Update PhotoViewer selection
        if hasattr(self.photo_viewer, "_on_photo_click"):
            self.photo_viewer._on_photo_click(photo_id)

        # Show single photo (pass both path and id)
        if hasattr(self.photo_viewer, "_show_single_photo"):
            photo_lbl = next(
                (lbl for lbl in self.photo_viewer.labels if lbl.photo_id == photo_id),
                None,
            )
            if photo_lbl:
                self.photo_viewer._show_single_photo(
                    photo_lbl.photo_path, photo_lbl.photo_id
                )

    def _scroll_to_label(self, lbl):
        """
        Scroll canvas to make the given thumbnail centered.

        Args:
            lbl: The label of the thumbnail to center.
        """
        canvas_width = self.canvas.winfo_width()
        lbl_x = lbl.winfo_x() + lbl.winfo_width() // 2
        scroll_x = max(0, lbl_x - canvas_width // 2)
        total_width = self.canvas.bbox("all")[2] if self.canvas.bbox("all") else 1
        self.canvas.xview_moveto(scroll_x / max(1, total_width))
