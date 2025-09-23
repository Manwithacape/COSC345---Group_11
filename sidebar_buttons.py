# sidebar_buttons.py
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Querybox
from tkinter import filedialog
import threading
from progress_dialog import ProgressDialog 

class SidebarButtons:
    """Holds logic for sidebar button actions."""

    def __init__(self, master, db=None, photo_viewer=None, importer=None):
        """
        :param master: Main application instance (tk.Tk or ttk.Window) with show_centered_info()
        :param db: Database instance
        :param photo_viewer: Photo viewer widget
        :param importer: PhotoImporter instance
        """
        self.master = master
        self.db = db
        self.photo_viewer = photo_viewer
        self.importer = importer
        self.buttons = []

    # ----------------- Helper to add button -----------------
    def add_button(self, sidebar, text, command):
        btn = ttk.Button(sidebar, text=text, bootstyle="primary", command=command)
        btn.pack(fill="x", pady=2, padx=5)
        self.buttons.append(btn)
        return btn

    # ----------------- Import -----------------
    def import_files(self):
        import tkinter as tk

        try:
            file_paths = filedialog.askopenfilenames(
                title="Select Photos",
                filetypes=[("Images", "*.jpg *.jpeg *.tif *.tiff *.cr2 *.nef *.arw *.dng *.rw2 *.orf *.raf *.srw *.pef"),
                           ("All Files", "*.*")]
            )
            if not file_paths:
                return

            if not self.importer:
                self.master.show_centered_info("Not Available", "Photo importer is not configured.")
                return

            # Input box for collection name
            collection_name = Querybox.get_string("Enter collection name:")
            if not collection_name:
                self.master.show_centered_info("No Name", "Collection name is required.")
                return

            collection_id = self.db.add_collection(collection_name)

            def do_import():
                dialog = ProgressDialog(self.master, title="Importing Photos", message="Importing photos, please wait...")
                dialog.start()

                def finish(success, imported_count=None, error=None):
                    # Always finish/close progress dialog
                    dialog.finish(success=success, imported_count=imported_count)
                    if success:
                        self.master.show_centered_info("Import Complete", f"Imported {imported_count} photos.")
                        if self.photo_viewer:
                            self.photo_viewer.refresh_photos(collection_id)
                    else:
                        self.master.show_centered_info("Import Error", str(error))

                try:
                    imported_count = self.importer.import_files(
                        list(file_paths),
                        collection_id,
                        default_styles=["General"]
                    )
                    self.master.after(0, lambda: finish(True, imported_count=imported_count))
                except Exception as e:
                    self.master.after(0, lambda: finish(False, error=e))

            threading.Thread(target=do_import, daemon=True).start()

        except Exception as e:
            self.master.show_centered_info("Import Error", str(e))

    # ----------------- Find Duplicates -----------------
    def find_duplicates(self):
        try:
            if not (self.importer and hasattr(self.importer, "duplicates")):
                self.master.show_centered_info("Not Available", "Duplicate detection is not configured.")
                return

            dialog = ProgressDialog(self.master, title="Finding Duplicates", message="Analyzing images...")
            dialog.start()

            def task():
                try:
                    duplicates_detector = self.importer.duplicates
                    photo_list = self.db.get_all_photos()  # list of dicts with 'id' and 'file_path'
                    duplicates_detector.find_duplicates_batch(photo_list)

                    self.master.after(0, lambda: (
                        dialog.finish(success=True),
                        self.master.show_centered_info("Duplicates Found", "Near-duplicate detection complete."),
                        self.photo_viewer.refresh_photos(None) if self.photo_viewer else None
                    ))
                except Exception as e:
                    self.master.after(0, lambda: (
                        dialog.finish(success=False),
                        self.master.show_centered_info("Error", f"Error finding duplicates: {e}")
                    ))

            threading.Thread(target=task, daemon=True).start()

        except Exception as e:
            self.master.show_centered_info("Error", f"Error finding duplicates: {e}")

    def switch_to_photos(self):
        """Switch to the PhotoViewer via the master."""
        if hasattr(self.master, "switch_to_photos"):
            self.master.switch_to_photos()
            if hasattr(self.master, "update_layout"):
                self.master.update_layout()

    def switch_to_collections(self):
        """Switch to the CollectionsViewer via the master."""
        if hasattr(self.master, "switch_to_collections"):
            self.master.switch_to_collections()
            if hasattr(self.master, "update_layout"):
                self.master.update_layout()

    # ----------------- Clear Duplicates (Dev) -----------------
    def clear_duplicates(self):
        """Development button: clear all duplicates in DB."""
        if self.db:
            self.db.clear_duplicates()
            self.master.show_centered_info("Duplicates Cleared", "All duplicates have been cleared.")
            if self.photo_viewer:
                self.photo_viewer.refresh_photos(None)

    # ------------------- Go Back Button ----------------
    def return_button(self):
        """Button for going back to the previous page"""
        if hasattr(self.master, "go_back"):
            self.master.go_back()
