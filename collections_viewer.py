# collections_viewer.py
import os
import ttkbootstrap as ttk
from PIL import Image, ImageTk, UnidentifiedImageError
from main_viewer import MainViewer

THUMBNAIL_SIZE = (90, 90)

class CollectionsViewer(MainViewer):
    """Scrollable list of collections with selection highlighting."""
    def __init__(self, parent, db, photo_viewer=None, switch_to_photos_callback=None, **kwargs):
        kwargs.pop("photo_viewer", None)
        kwargs.pop("switch_to_photos_callback", None)
        super().__init__(parent, **kwargs)
        
   
        self.db = db
        self.photo_viewer = photo_viewer
        self.switch_to_photos_callback = switch_to_photos_callback


        self.collection_rows = []
        self.collection_ids = []
        self._thumbnail_cache = {}  # {collection_id: PhotoImage}
        self.selected_idx = None

        self.refresh_collections()

    def get_thumbnail(self, coll: dict) -> str | None:
        """Return a filesystem path to a cover image for this collection."""
        try:
            row = self.db.get_first_photo_for_collection(coll["id"])
            if not row:
                return None
            # Adjust column name if your table differs
            p = row.get("path") or row.get("file_path")
            if not p:
                return None
            # Normalise to absolute path if needed
            p = os.path.abspath(p)
            if os.path.exists(p):
                return p
        except Exception as e:
            print(f"[thumb] Failed to fetch thumbnail path for coll {coll.get('id')}: {e}")
        return None

    def _load_thumbnail(self, path: str) -> ImageTk.PhotoImage:
        """Open, thumbnail, and wrap as PhotoImage."""
        try:
            with Image.open(path) as img:
                img = img.convert("RGB")
                img.thumbnail(THUMBNAIL_SIZE)
                return ImageTk.PhotoImage(img)
        except UnidentifiedImageError:
            # Happens for unsupported formats (e.g., RAW/HEIC without plugins)
            raise
        except Exception:
            raise

    def refresh_collections(self):
        """Reload collection list from DB and (re)build the UI rows."""
        for row in self.collection_rows:
            row.destroy()
        self.collection_rows.clear()
        self.collection_ids.clear()
        self.selected_idx = None

        collections = self.db.get_collections() or []

        # Create a single horizontal container frame
        if hasattr(self, "collections_row"):
            self.collections_row.destroy()
            
        self.collections_row = ttk.Frame(self.inner_frame)
        self.collections_row.pack(fill="x", pady=10)
        self.collection_rows.append(self.collections_row)
        
        

        for idx, coll in enumerate(collections):
            if idx > 0 and idx % 5 == 0:
                self.collections_row = ttk.Frame(self.inner_frame)
                self.collections_row.pack(fill="x", pady=10)
                self.collection_rows.append(self.collections_row)

            card = ttk.Frame(self.collections_row, padding=10, bootstyle="secondary")
            card.pack(side="left", padx=8, pady=2)
            self.collection_ids.append(coll["id"])
            thumb_lbl = ttk.Label(card)
            thumb_lbl.pack(side="top")

            path = self.get_thumbnail(coll)
            if path:
                try:
                    ph = self._thumbnail_cache.get(coll["id"])
                    if ph is None:
                        ph = self._load_thumbnail(path)
                        self._thumbnail_cache[coll["id"]] = ph
                    thumb_lbl.configure(image=ph)
                    thumb_lbl.image = ph  # keep reference to avoid GC
                except Exception as e:
                        print(f"[thumb] Error loading '{path}' for coll {coll['id']}: {e}")
                        thumb_lbl.configure(text="[Error loading thumbnail]")
            else:
                thumb_lbl.configure(text="[No thumbnail]")

                # NAME (below or above thumbnail)
            name_lbl = ttk.Label(card, text=coll["name"], anchor="center", padding=(0, 5))
            name_lbl.pack(side="top", fill="x")

                # Click bindings
            for w in (card, thumb_lbl, name_lbl):
                w.bind("<Double-1>", lambda e, i=idx: self._on_collection_double_click(i))
            
            
    
  
    def _on_collection_double_click(self, idx: int):
        """Double-click: refresh PhotoViewer and switch to it safely."""
        collection_id = self.collection_ids[idx]
        if self.switch_to_photos_callback:
            def update_view():
                if self.photo_viewer:
                    self.photo_viewer.refresh_photos(collection_id)
                self.switch_to_photos_callback()
            self.after(0, update_view)
