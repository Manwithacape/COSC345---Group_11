# sidebar_buttons.py
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox, Querybox
from tkinter import filedialog
import threading

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
        self.buttons = []

    # ----------------- Helper to add button -----------------
    def add_button(self, sidebar, text, command):
        btn = ttk.Button(sidebar, text=text, bootstyle="primary", command=command)
        btn.pack(fill="x", pady=2, padx=5)
        self.buttons.append(btn)
        return btn

    # ----------------- Import -----------------
    def import_files(self):
        import threading
        try:
            file_paths = filedialog.askopenfilenames(
                title="Select Photos",
                filetypes=[("Images", "*.jpg *.jpeg *.tif *.tiff *.cr2 *.nef *.arw *.dng *.rw2 *.orf *.raf *.srw *.pef"), ("All Files", "*.*")]
            )
            if not file_paths:
                return

            if not self.importer:
                Messagebox.show_warning("Not Available", "Photo importer is not configured.")
                return

            # Always import into a new collection
            collection_id = self.db.add_collection("Imported from Sidebar")

            def do_import():
                import time
                import tkinter as tk
                from ttkbootstrap import Progressbar
                progress_win = tk.Toplevel(self.master)
                progress_win.title("Importing Photos...")
                progress_win.geometry("300x80")
                progress_win.transient(self.master)
                progress_win.grab_set()
                # Center the progress window
                progress_win.update_idletasks()
                screen_width = progress_win.winfo_screenwidth()
                screen_height = progress_win.winfo_screenheight()
                x = (screen_width // 2) - (300 // 2)
                y = (screen_height // 2) - (80 // 2)
                progress_win.geometry(f"300x80+{x}+{y}")
                label = ttk.Label(progress_win, text="Importing photos, please wait...")
                label.pack(pady=10)
                pb = Progressbar(progress_win, mode="indeterminate")
                pb.pack(fill="x", padx=20, pady=5)
                pb.start(10)
                def finish(success, imported_count=None, error=None):
                    pb.stop()
                    progress_win.destroy()
                    if success:
                        Messagebox.show_info("Import Complete", f"Imported {imported_count} photos.")
                        self.photo_viewer.refresh_photos(collection_id)
                    else:
                        Messagebox.show_error("Import Error", str(error))
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


    def switch_to_photos(self):
        """Switch to the PhotoViewer via the master."""
        if hasattr(self.master, "switch_to_photos"):
            self.master.switch_to_photos()
            # Ensure photo_viewer is the active viewer and layout is updated
            if hasattr(self.master, "update_layout"):
                self.master.update_layout()

    def switch_to_collections(self):
        """Switch to the CollectionsViewer via the master."""
        if hasattr(self.master, "switch_to_collections"):
            self.master.switch_to_collections()
            # Ensure collections_viewer is the active viewer and layout is updated
            if hasattr(self.master, "update_layout"):
                self.master.update_layout()

    # ----------------- Clear Duplicates (Dev) -----------------
    def clear_duplicates(self):
        """Development button: clear all duplicates in DB."""
        if self.db:
            self.db.clear_duplicates()
            Messagebox.show_info("Duplicates Cleared", "All duplicates have been cleared.")
            if self.photo_viewer:
                self.photo_viewer.refresh_photos(None)
