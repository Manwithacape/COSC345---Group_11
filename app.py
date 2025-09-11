import tkinter as tk
from tkinter import filedialog, messagebox
from gui import Sidebar
from db import Database
from photo_importer import PhotoImporter
from photo_viewer import PhotoViewer
from collections_viewer import CollectionsViewer
from filmstrip_viewer import FilmstripViewer
from exif_viewer import ExifViewer
from score_viewer import ScoreViewer
from duplicate_viewer import DuplicateViewer
from sidebar_buttons import SidebarButtons


class AutoCullApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AutoCull")
        self.geometry("1200x800")
        self.configure(bg="#1e1e1e")

        # Database
        self.db = Database()
        self.db.create_schema()

        # Importer
        self.importer = PhotoImporter(self.db)

        # Track which central viewer is active
        self.active_viewer = None

        # Setup menubar
        self.setup_menubar()

        # Default view is PhotoViewer
        self.photo_viewer = PhotoViewer(self, self.db, bg="#141414")
        self.collections_viewer = CollectionsViewer(self, self.db, bg="#141414")

        

        # Buttons logic handler
        self.sidebar_buttons = SidebarButtons(
            master=self,
            db=self.db,
            photo_viewer=self.photo_viewer,
            importer=self.importer
        )

        # Left sidebar (with buttons)
        self.left_sidebar = Sidebar(
            self,
            side="left",
            db=self.db,
            bg="#2f2f2f",
            photo_viewer=self.photo_viewer,
            importer=self.importer
        )
        self.left_sidebar.pack(side="left", fill="y")

        # Right sidebar
        self.right_sidebar = Sidebar(self, side="right", bg="#2f2f2f")
        self.exif_viewer = ExifViewer(self.right_sidebar, self.db, bg="#2f2f2f")
        self.exif_viewer.pack(fill="both", expand=True, padx=5, pady=5)

        self.score_viewer = ScoreViewer(self.right_sidebar, self.db, bg="#2f2f2f")
        self.score_viewer.pack(fill="both", expand=True, padx=5, pady=5)

        self.filmstrip = FilmstripViewer(
            self,
            self.photo_viewer,
            exif_viewer=self.exif_viewer,
            score_viewer=self.score_viewer
        )
        self.filmstrip.pack(fill="x", side="bottom")

        self.duplicate_viewer = DuplicateViewer(self.right_sidebar, self.db, bg="#2f2f2f")
        self.duplicate_viewer.pack(fill="both", expand=True, padx=5, pady=5)

        # Keep layout updated
        self.bind("<Configure>", lambda e: self.update_layout())
        self.update_layout()
        
        self.switch_to_photos()

    # ---------- Layout ----------
    def update_layout(self):
        w, h = self.winfo_width(), self.winfo_height()

        # Filmstrip height
        fh = self.filmstrip.winfo_reqheight() or 120  # fallback default height

        # Left sidebar
        lw = self.left_sidebar.width if not self.left_sidebar.collapsed else 30
        self.left_sidebar.place(x=0, y=0, width=lw, height=h - fh)
        self.left_sidebar.lift()

        # Right sidebar
        rw = self.right_sidebar.width if not self.right_sidebar.collapsed else 30
        self.right_sidebar.place(x=max(0, w - rw), y=0, width=rw, height=h - fh)
        self.right_sidebar.lift()

        # Active viewer fills between sidebars above filmstrip
        if self.active_viewer:
            pv_x = lw
            pv_width = max(0, w - lw - rw)
            self.active_viewer.place(x=pv_x, y=0, width=pv_width, height=h - fh)

        # Filmstrip always full width at bottom
        self.filmstrip.place(x=0, y=h - fh, width=w, height=fh)

        # Update toggle icons
        self.left_sidebar.toggle_btn.config(text="⮞" if self.left_sidebar.collapsed else "⮜")
        self.right_sidebar.toggle_btn.config(text="⮜" if self.right_sidebar.collapsed else "⮞")

    # ---------- Menubar ----------
    def setup_menubar(self):
        menubar = tk.Menu(self)

        # File
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Collection", command=lambda: print("New Collection"))
        file_menu.add_command(label="Open Collection...", command=lambda: print("Open"))
        file_menu.add_separator()
        # Hook menu import to the SidebarButtons version
        file_menu.add_command(label="Import Photos", command=self.sidebar_import_photos)
        file_menu.add_command(label="Export Selection", command=lambda: print("Export"))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Preferences", command=lambda: print("Preferences"))
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Collections
        collections_menu = tk.Menu(menubar, tearoff=0)
        collections_menu.add_command(label="View Photos", command=self.switch_to_photos)
        collections_menu.add_command(label="View Collections", command=self.switch_to_collections)
        menubar.add_cascade(label="Collections", menu=collections_menu)

        # Attach menubar
        self.config(menu=menubar)

    # ---------- Import wrapper for menubar ----------
    def sidebar_import_photos(self):
        """Call the SidebarButtons import handler (so logic stays centralized)."""
        self.sidebar_buttons.import_files()

    # ---------- Switch views ----------
    def switch_to_photos(self):
        if self.active_viewer:
            self.active_viewer.place_forget()
        self.active_viewer = self.photo_viewer
        self.update_layout()

    def switch_to_collections(self):
        if self.active_viewer:
            self.active_viewer.place_forget()
        self.active_viewer = self.collections_viewer
        self.collections_viewer.refresh_collections()
        self.update_layout()


if __name__ == "__main__":
    app = AutoCullApp()
    app.mainloop()
