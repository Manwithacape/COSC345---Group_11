import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox
from tkinter import filedialog
from gui import Sidebar
from db import Database
from photo_importer import PhotoImporter
from photo_viewer import PhotoViewer
from filmstrip_viewer import FilmstripViewer
from exif_viewer import ExifViewer
from score_viewer import ScoreViewer
from duplicate_viewer import DuplicateViewer
from custom_menubar import CustomMenuBar
from custom_toolbar import CustomToolbar


class AutoCullApp(tb.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        # self.overrideredirect(True)
        self.title("AutoCull")
        self.geometry("1200x800")
        self.configure(bg="#1e1e1e")

        # Database
        self.db = Database()
        self.db.create_schema()

        # Importer
        self.importer = PhotoImporter(self.db)

        # Setup menubar
        # self.setup_menubar()  # Remove menubar, use toolbar instead
        self.toolbar = CustomToolbar(self)
        self.toolbar_height = 40  # Adjust as needed for your toolbar
        self.toolbar.place(x=0, y=0, relwidth=1, height=self.toolbar_height)

        # Center photo viewer
        self.photo_viewer = PhotoViewer(self, self.db)
        # Don't pack, use place in update_layout

        # Sidebars
        self.left_sidebar = Sidebar(
            self,
            side="left",
            db=self.db,
            photo_viewer=self.photo_viewer,
            import_command=self.import_photos
        )

        # Right sidebar
        self.right_sidebar = Sidebar(self, side="right")
        self.exif_viewer = ExifViewer(self.right_sidebar, self.db)
        self.exif_viewer.pack(fill="both", expand=True, padx=5, pady=5)

        self.score_viewer = ScoreViewer(self.right_sidebar, self.db)
        self.score_viewer.pack(fill="both", expand=True, padx=5, pady=5)

        self.filmstrip = FilmstripViewer(
            self, 
            self.photo_viewer, 
            exif_viewer=self.exif_viewer, 
            score_viewer=self.score_viewer
        )
        self.filmstrip.pack(fill="x", side="bottom")

        self.duplicate_viewer = DuplicateViewer(self.right_sidebar, self.db)
        self.duplicate_viewer.pack(fill="both", expand=True, padx=5, pady=5)

        # Keep layout updated
        self.bind("<Configure>", lambda e: self.update_layout())
        self.update_layout()

    # ---------- Layout ----------
    def update_layout(self):
        w, h = self.winfo_width(), self.winfo_height()
        th = getattr(self, 'toolbar_height', 40)

        # Left sidebar
        lw = self.left_sidebar.width if not self.left_sidebar.collapsed else 30
        self.left_sidebar.place(x=0, y=th, width=lw, height=h-th)
        self.left_sidebar.lift()

        # Right sidebar
        rw = self.right_sidebar.width if not self.right_sidebar.collapsed else 30
        self.right_sidebar.place(x=max(0, w - rw), y=th, width=rw, height=h-th)
        self.right_sidebar.lift()

        # Photo viewer takes the gap between sidebars
        pv_x = lw
        pv_width = max(0, w - lw - rw)
        self.photo_viewer.place(x=pv_x, y=th, width=pv_width, height=h-th)

        # Update toggle icons
        self.left_sidebar.toggle_btn.config(text="⮞" if self.left_sidebar.collapsed else "⮜")
        self.right_sidebar.toggle_btn.config(text="⮜" if self.right_sidebar.collapsed else "⮞")

    # ---------- Menubar ----------
    def setup_menubar(self):
        menubar = CustomMenuBar(self)
        self.config(menu=menubar)

    # ---------- Import ----------
    def import_photos(self):
        folder_path = filedialog.askdirectory(title="Select Photo Folder")
        if not folder_path:
            return

        # Create a collection for the import
        collection_id = self.db.add_collection("Imported Collection")

        try:
            imported_count = self.importer.import_folder(
                folder_path, collection_id, default_styles=["Travel"]
            )
            Messagebox.show_info(f"Imported {imported_count} photos.", title="Import Complete")
        except Exception as e:
            Messagebox.show_error(str(e), title="Import Error")

        # Refresh viewer
        self.photo_viewer.refresh_photos(collection_id)
        self.filmstrip.refresh_thumbs()

    


if __name__ == "__main__":
    app = AutoCullApp()
    app.mainloop()
