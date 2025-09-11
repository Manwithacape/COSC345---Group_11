import ttkbootstrap as ttk
from main_viewer import MainViewer

class CollectionsViewer(MainViewer):
    """Scrollable list of collections"""

    def __init__(self, parent, db, photo_viewer=None, switch_to_photos_callback=None, **kwargs):
        """
        :param switch_to_photos_callback: function to call when double-clicking a collection
        """
        super().__init__(parent, **kwargs)
        self.db = db
        self.photo_viewer = photo_viewer
        self.switch_to_photos_callback = switch_to_photos_callback

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
            lbl = ttk.Label(
                self.inner_frame,
                text=coll["name"],
                anchor="w",
                padding=(10,5),
                cursor="hand2",
                bootstyle="secondary"
            )
            lbl.collection_id = coll["id"]
            lbl.bind("<Button-1>", lambda e, cid=coll["id"], i=idx: self._on_collection_click(cid, i))
            lbl.bind("<Double-1>", lambda e, cid=coll["id"]: self._on_collection_double_click(cid))
            lbl.pack(fill="x", pady=2)
            self.collection_labels.append(lbl)

    def _on_collection_click(self, collection_id, idx):
        """Handle selecting a collection (single click)."""
        if self.selected_idx is not None and 0 <= self.selected_idx < len(self.collection_labels):
            self.collection_labels[self.selected_idx].config(bootstyle="secondary")

        self.selected_idx = idx
        self.collection_labels[idx].config(bootstyle="dark")  # highlight

        if self.photo_viewer:
            self.photo_viewer.refresh_photos(collection_id)

    def _on_collection_double_click(self, collection_id):
        """Double-click handler: switch to PhotoViewer for this collection."""
        if self.photo_viewer:
            # Refresh PhotoViewer with the selected collection
            self.photo_viewer.refresh_photos(collection_id)
        
        # Call the callback to switch the main viewer
        if self.switch_to_photos_callback:
            self.switch_to_photos_callback()  # ensures active_viewer = photo_viewer and layout updates
