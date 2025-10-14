# sidebar_buttons.py
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Querybox, Messagebox
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
        self.cull_button = None
        self.suggestions_button = None
        self.suggestions_visible = False

    # ----------------- Helper to add button -----------------
    def add_button(self, sidebar, text, command):
        btn = ttk.Button(sidebar, text=text, bootstyle="primary", command=command)
        btn.pack(fill="x", pady=2, padx=5)
        self.buttons.append(btn)
        return btn

    # ----------------- Import -----------------
    def import_files(self):
        more_directories = True
        file_paths = []

        try:
            file_paths = filedialog.askopenfilenames(
                title="Select Photos",
                filetypes=[
                    (
                        "Images",
                        "*.jpg *.jpeg *.tif *.tiff *.cr2 *.nef *.arw *.dng *.rw2 *.orf *.raf *.srw *.pef",
                    ),
                    ("All Files", "*.*"),
                ],
            )

            while more_directories:
                if not file_paths:
                    return
                resp = Messagebox.yesno(
                    "Do you want to add photos from another directory?", "More Photos"
                )
                if resp == "Yes":
                    additional_files = filedialog.askopenfilenames(
                        title="Select More Photos",
                        filetypes=[
                            (
                                "Images",
                                "*.jpg *.jpeg *.tif *.tiff *.cr2 *.nef *.arw *.dng *.rw2 *.orf *.raf *.srw *.pef",
                            ),
                            ("All Files", "*.*"),
                        ],
                    )
                    if additional_files:
                        file_paths = list(file_paths) + list(additional_files)
                else:
                    more_directories = False
            # Need to put in here how to import multiple files from different directories
            if not file_paths:
                return

            if not self.importer:
                self.master.show_centered_info(
                    "Not Available", "Photo importer is not configured."
                )
                return

            # Input box for collection name
            collection_name = Querybox.get_string("Enter collection name:")
            if not collection_name:
                self.master.show_centered_info(
                    "No Name", "Collection name is required."
                )
                return

            # Ensure unique collection name (UI-level check)
            while hasattr(self.db, "collection_exists") and self.db.collection_exists(collection_name):
                self.master.show_centered_info(
                    "Name Taken",
                    "A collection with that name already exists. \n Please choose a different name.",
                )
                collection_name = Querybox.get_string("Enter collection name:")
            

            collection_id = self.db.add_collection(collection_name)
            if collection_id is None:
                # Fallback safeguard if DB-level unique constraint blocked the insert
                self.master.show_centered_info(
                    "Name Taken",
                    "A collection with that name already exists. Please choose a different name.",
                )
                return

            def do_import():
                dialog = ProgressDialog(
                    self.master,
                    title="Importing Photos",
                    message="Importing photos, please wait...",
                )
                dialog.start()

                def finish(success, imported_count=None, error=None):
                    # Always finish/close progress dialog
                    dialog.finish(success=success, imported_count=imported_count)
                    if success:
                        self.master.show_centered_info(
                            "Import Complete", f"Imported {imported_count} photos."
                        )
                        if self.photo_viewer:
                            self.photo_viewer.refresh_photos(collection_id)
                    else:
                        self.master.show_centered_info("Import Error", str(error))

                try:
                    imported_count = self.importer.import_files(
                        list(file_paths), collection_id, default_styles=["General"]
                    )
                    self.master.after(
                        0, lambda: finish(True, imported_count=imported_count)
                    )
                except Exception as e:
                    self.master.after(0, lambda: finish(False, error=e))

            threading.Thread(target=do_import, daemon=True).start()

        except Exception as e:
            self.master.show_centered_info("Import Error", str(e))

    # ----------------- Find Duplicates -----------------
    def find_duplicates(self):
        try:
            if not (self.importer and hasattr(self.importer, "duplicates")):
                self.master.show_centered_info(
                    "Not Available", "Duplicate detection is not configured."
                )
                return

            dialog = ProgressDialog(
                self.master, title="Finding Duplicates", message="Analyzing images..."
            )
            dialog.start()

            def task():
                try:
                    duplicates_detector = self.importer.duplicates
                    photo_list = (
                        self.db.get_all_photos()
                    )  # list of dicts with 'id' and 'file_path'
                    duplicates_detector.find_duplicates_batch(photo_list)

                    self.master.after(
                        0,
                        lambda: (
                            dialog.finish(success=True),
                            self.master.show_centered_info(
                                "Duplicates Found", "Near-duplicate detection complete."
                            ),
                            (
                                self.photo_viewer.refresh_photos(None)
                                if self.photo_viewer
                                else None
                            ),
                        ),
                    )
                except Exception as e:
                    self.master.after(
                        0,
                        lambda: (
                            dialog.finish(success=False),
                            self.master.show_centered_info(
                                "Error", f"Error finding duplicates: {e}"
                            ),
                        ),
                    )

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
            self.master.show_centered_info(
                "Duplicates Cleared", "All duplicates have been cleared."
            )
            if self.photo_viewer:
                self.photo_viewer.refresh_photos(None)

    # ------------------- Go Back Button ----------------
    def return_button(self):
        """Button for going back to the previous page"""
        if hasattr(self.master, "go_back"):
            self.master.go_back()

    # ------------------- Suggestion Logic ----------------
    def show_suggestions(self):
        """
        Suggest 'keep' for best duplicate, 'delete' for others.
        Suggest 'delete' for low-quality photos.
        """
        try:
            if not self.importer:
                self.master.show_centered_info("Not Available", "Photo importer is not configured.")
                return
            
            dialog = ProgressDialog(self.master, title="Generating Suggestions", message="Analyzing photos...")
            dialog.start()

            def task():
                try:
                    # photo_list = self.db.get_all_photos()  # list of dicts with 'id' and 'file_path'
                    photo_list = [
                        p for p in self.db.get_all_photos()
                        if (p.get("suggestion") or "").lower() != "deleted"
                    ]

                    # if not photo_list:
                    #     self.master.master.after(0, lambda:(
                    #         dialog.finish(success=False),
                    #         self.master.show_centered_info(
                    #         "No Photos", "There are no photos to analyze.")
                    #     ))
                    #     return

                    existing_groups = self.db.get_near_duplicate_groups()
                    ungrouped_photos = self.db.get_photos_without_duplicate_group()

                    if ungrouped_photos:
                        print("[INFO] Found {len(ungrouped_photos)} ungrouped photos, running partial duplicate detection.")
                        if hasattr(self.importer, "duplicates"):
                            duplicates = self.importer.duplicates
                            # Collect all photos already in groups to include in detection
                            grouped_photos = [photo for group in existing_groups for photo in group["photos"]]
                            duplicates.find_duplicates_batch(ungrouped_photos + grouped_photos)
                            existing_groups = self.db.get_near_duplicate_groups()
                    else:
                        print(f"[INFO] Found {len(existing_groups)} duplicate groups - using existing results.")
                    
                    group_map = {g["id"]: g["photos"] for g in existing_groups}
                    handled_ids = set()

                    for group_id, photos in group_map.items():
                        if not photos:
                            continue
                        
                        best = max(photos, key=lambda p: p.get("score", 0) or 0)
                        for p in photos:
                            if (p.get("suggestion") or "").lower() == "deleted":
                                continue
                            pid = p["id"]
                            sugg = "keep" if pid == best["id"] else "delete"
                            self.db.update_photo_suggestion(pid, sugg)
                            handled_ids.add(pid)

                    for photo in photo_list:
                        current_suggestion = (photo.get("suggestion") or "").lower()

                        if (photo.get("suggestion") or "").lower() == "deleted":
                            continue

                        # Skip if already has a non-undecided suggestion
                        if current_suggestion in {"keep", "delete"}:
                            continue

                        # Skip if already handled in a duplicate group
                        pid = photo["id"]
                        if pid in handled_ids:
                            continue

                        # Otherwise, suggest based on quality score
                        score = photo.get("score", 0.0)
                        if score < 0.4:
                            suggestion = "delete"
                        elif score > 0.7:
                            suggestion = "keep"
                        else:
                            suggestion = "undecided"
                        
                        # Only update if suggestion changed
                        if suggestion != current_suggestion:
                            self.db.update_photo_suggestion(pid, suggestion)

                    self.master.after(0, lambda: (
                        dialog.finish(success=True),
                        self.master.show_centered_info("Suggestions Complete", "Photo suggestions have been updated."),
                        self.photo_viewer.refresh_photos(None) if self.photo_viewer else None
                    ))

                except Exception as e:
                    self.master.after(0, lambda e=e: (
                        dialog.finish(success=False),
                        self.master.show_centered_info("Error", f"Error generating suggestions: {e}")
                    ))

            threading.Thread(target=task, daemon=True).start()
        except Exception as e:
            self.master.show_centered_info("Error", f"Error generating suggestions: {e}")

    # ------------------- Cull Photos ----------------
    def cull_photos(self):
        """Delete all photos marked as 'delete' in the database"""

        if not Messagebox.yesno("Delete all photos marked 'delete'?", "Cull Photos"):
            return
        
        photos = self.db.get_photos_by_suggestion('delete')
        if not photos:
            Messagebox.show_info("Cull Photos", "No photos marked 'delete' found.")
            return
        
        deleted_count = 0
        errors = []

        for row in photos:
            photo_id = row["id"] if isinstance(row, dict) else row[0]
            try:
                # Temporarily set context and delete
                self.photo_viewer._ctx_photo_id = photo_id
                self.photo_viewer._ctx_delete_selected(confirm=False)
                deleted_count += 1
            except Exception as e:
                errors.append(f"Error deleting photo ID {photo_id}: {e}")

        summary = f"Deleted {deleted_count} photos."
        if errors:
            summary += "\nSome errors occured:\n" + "\n".join(errors[:10])

        Messagebox.show_info("Cull Photos", summary)

        # Refresh UI once at the end 
        try:
            self.photo_viewer.refresh_photos()
        except Exception:
            if hasattr(self.master, "update_layout"):
                self.master.update_layout()

    def toggle_suggestions(self):
        """Toggle suggestions view and Cull button visibility."""
        if not self.suggestions_visible:
            # Run show_suggestions normally
            self.show_suggestions()
            # Show Cull button
            if self.cull_button:
                self.cull_button.pack(fill="x", pady=2, padx=5)
            # Change button text
            if self.suggestions_button:
                self.suggestions_button.config(text="Hide Suggestions")
            self.suggestions_visible = True
        else:
            # Hide Cull button
            if self.cull_button:
                self.cull_button.pack_forget()
            # Change button text back
            if self.suggestions_button:
                self.suggestions_button.config(text="Show Suggestions")
            self.suggestions_visible = False
 
        if self.photo_viewer:
            self.photo_viewer.refresh_photos(self.photo_viewer.current_collection_id)