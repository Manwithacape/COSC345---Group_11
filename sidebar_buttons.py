# sidebar_buttons.py
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox, Querybox
from tkinter import filedialog

class SidebarButtons:
    """Holds logic for sidebar button actions."""

    def __init__(self, master, db=None, photo_viewer=None, importer=None):
        """
        :param master: Main application instance (tk.Tk)
        :param db: Database instance
        :param photo_viewer: Photo viewer widget
        :param importer: PhotoImporter instance
        """
        self.master = master
        self.db = db
        self.photo_viewer = photo_viewer
        self.importer = importer

    # ----------------- Import -----------------
    def import_files(self):
        try:
            file_paths = filedialog.askopenfilenames(
                title="Select Photos",
                filetypes=[("Images", "*.jpg *.jpeg *.tif *.tiff")]
            )
            if not file_paths:
                return

            if not self.importer:
                Messagebox.show_warning("Not Available", "Photo importer is not configured.")
                return

            # Always import into a new collection
            collection_id = self.db.add_collection("Imported from Sidebar")

            imported_count = self.importer.import_files(
                list(file_paths), 
                collection_id,
                default_styles=["General"]
            )

            # Refresh viewer
            self.photo_viewer.refresh_photos(collection_id)

            Messagebox.show_info("Import Complete", f"Imported {imported_count} photos.")

        except Exception as e:
            Messagebox.show_error("Import Error", str(e))

    # ----------------- Find Duplicates -----------------
    def find_duplicates(self):
        try:
            if not (self.importer and hasattr(self.importer, "duplicates")):
                Messagebox.show_warning("Not Available", "Duplicate detection is not configured.")
                return

            duplicates_detector = self.importer.duplicates
            photo_list = self.db.get_all_photos()  # list of dicts with 'id' and 'file_path'
            duplicates_detector.find_duplicates_batch(photo_list)

            Messagebox.show_info(
                "Duplicates Found",
                "Near-duplicate detection complete."
            )

            # Refresh viewer
            self.photo_viewer.refresh_photos(None)

        except Exception as e:
            Messagebox.show_error("Error", f"Error finding duplicates: {e}")
