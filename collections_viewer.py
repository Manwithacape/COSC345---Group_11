# collections_viewer.py
import ttkbootstrap as ttk
from main_viewer import MainViewer

class CollectionsViewer(MainViewer):
    """Scrollable list of collections with selection highlighting."""

    def __init__(self, parent, db, photo_viewer=None, switch_to_photos_callback=None, **kwargs):
        kwargs.pop("photo_viewer", None)
        kwargs.pop("switch_to_photos_callback", None)
        super().__init__(parent, **kwargs)

        self.db = db
        self.photo_viewer = photo_viewer
        self.switch_to_photos_callback = switch_to_photos_callback

        self.collection_labels = []
        self.selected_idx = None
        self.refresh_collections()

    def refresh_collections(self):
        """Reload collection list from DB."""
        for lbl in self.collection_labels:
            lbl.destroy()
        self.collection_labels.clear()

        collections = self.db.get_collections()
        for idx, coll in enumerate(collections):
            lbl = ttk.Label(
                self.inner_frame,
                text=coll["name"],
                anchor="w",
                padding=(10, 5),
                cursor="hand2",
                bootstyle="secondary"
            )
            lbl.collection_id = coll["id"]
            lbl.bind("<Button-1>", lambda e, cid=coll["id"], i=idx: self._on_collection_click(cid, i))
            lbl.bind("<Double-1>", lambda e, cid=coll["id"]: self._on_collection_double_click(cid))
            lbl.pack(fill="x", pady=2)
            self.collection_labels.append(lbl)

    def _on_collection_click(self, collection_id, idx):
        """Single-click: highlight collection and refresh PhotoViewer."""
        if self.selected_idx is not None and 0 <= self.selected_idx < len(self.collection_labels):
            self.collection_labels[self.selected_idx].config(bootstyle="secondary")
        self.selected_idx = idx
        self.collection_labels[idx].config(bootstyle="dark")

        if self.photo_viewer:
            self.photo_viewer.refresh_photos(collection_id)

    def _on_collection_double_click(self, collection_id):
        """Double-click: refresh PhotoViewer and switch to it safely."""
        if self.switch_to_photos_callback:
            def update_view():
                if self.photo_viewer:
                    self.photo_viewer.refresh_photos(collection_id)
                self.switch_to_photos_callback()
            self.after(0, update_view)
