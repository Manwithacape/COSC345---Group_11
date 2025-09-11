import tkinter as tk
from main_viewer import MainViewer

class CollectionsViewer(MainViewer):
    """Scrollable list of collections. Clicking loads photos."""

    def __init__(self, parent, db, photo_viewer=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.db = db
        self.photo_viewer = photo_viewer

        self.collection_labels = []
        self.selected_idx = None
        self.refresh_collections()

    def refresh_collections(self):
        """Reload collections list from DB."""
        for lbl in self.collection_labels:
            lbl.destroy()
        self.collection_labels.clear()

        collections = self.db.get_collections()
        for idx, coll in enumerate(collections):
            lbl = tk.Label(
                self.inner_frame,
                text=coll["name"],
                bg="#2f2f2f",
                fg="white",
                anchor="w",
                padx=10,
                pady=5,
                cursor="hand2",
            )
            lbl.collection_id = coll["id"]
            lbl.bind("<Button-1>", lambda e, cid=coll["id"], i=idx: self._on_collection_click(cid, i))
            lbl.pack(fill="x", pady=2)
            self.collection_labels.append(lbl)

    def _on_collection_click(self, collection_id, idx):
        """Handle selecting a collection and refresh PhotoViewer."""
        if self.selected_idx is not None and 0 <= self.selected_idx < len(self.collection_labels):
            self.collection_labels[self.selected_idx].config(bg="#2f2f2f")

        self.selected_idx = idx
        self.collection_labels[idx].config(bg="#454545")  # highlight

        if self.photo_viewer:
            self.photo_viewer.refresh_photos(collection_id)
