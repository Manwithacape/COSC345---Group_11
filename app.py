"""
AutoCull Main Application

This file launches the AutoCull photo culling and scoring GUI.
Features:
- Darkly themed interface using ttkbootstrap
- Sidebar navigation and viewers for photos, collections, EXIF, scores, duplicates
- Splash screen and window centering
- Database integration and automatic schema creation
- Handles RAW and standard image formats

Run this file to start the application.
"""
import os, sys
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox, Querybox
from tkinter import filedialog
from gui import Sidebar
from db import Database
from photo_importer import PhotoImporter
from photo_viewer import PhotoViewer
from single_photo_viewer import SinglePhotoViewer
from collections_viewer import CollectionsViewer
from filmstrip_viewer import FilmstripViewer
from exif_viewer import ExifViewer
from score_viewer import ScoreViewer
from duplicate_viewer import DuplicateViewer
from sidebar_buttons import SidebarButtons
from scrollable_frame import ScrollableFrame
from faces_frame import FacesFrame
import tkinter as tk

# Pillow for loading .webp logo
try:
    from PIL import Image, ImageTk
    _HAS_PIL = True
except Exception:
    _HAS_PIL = False


class AutoCullApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("AutoCull")
        self.geometry("1200x800")

        # Database
        self.db = Database()
        self.db.create_schema()

        # Importer
        self.importer = PhotoImporter(self.db)

        # Track which central viewer is active
        self.active_viewer = None

        # Setup menubar
        self.setup_menubar()

        # ---------- Create viewers first ----------
        self.photo_viewer = PhotoViewer(
            self, self.db, open_single_callback=self.open_single_view
        )
        self.collections_viewer = CollectionsViewer(
            self,
            self.db,
            photo_viewer=self.photo_viewer,
            switch_to_photos_callback=lambda: self.after(0, self._switch_to_photos),
        )

        # ---------- Back button (hidden by default) ----------
        self.back_btn = ttk.Button(
            self, text="⮜ Back", bootstyle="secondary", command=self._switch_to_photos
        )
        self.back_btn.place_forget()

        # ---------- Sidebar buttons logic ----------
        self.sidebar_buttons = SidebarButtons(
            master=self,
            db=self.db,
            photo_viewer=self.photo_viewer,
            importer=self.importer,
        )

        # ---------- Left sidebar ----------
        self.left_sidebar = Sidebar(self, side="left", db=self.db)
        self.sidebar_buttons.add_button(
            self.left_sidebar.body, "View Photos", lambda: self.after(0, self._switch_to_photos)
        )
        self.sidebar_buttons.add_button(
            self.left_sidebar.body, "View Collections", lambda: self.after(0, self._switch_to_collections)
        )
        self.sidebar_buttons.add_button(
            self.left_sidebar.body, "Import Photos", self.sidebar_buttons.import_files
        )
        self.sidebar_buttons.add_button(
            self.left_sidebar.body, "Find Duplicates", self.sidebar_buttons.find_duplicates
        )
        self.sidebar_buttons.add_button(
            self.left_sidebar.body, "Clear Duplicates (Dev)", self.sidebar_buttons.clear_duplicates
        )
        self.sidebar_buttons.add_button(
            self.left_sidebar.body, "Return", self.sidebar_buttons.return_button
        )
        self.left_sidebar.pack(side="left", fill="y")

        # ---------- Right sidebar & other viewers (scrollable) ----------
        self.right_sidebar = Sidebar(self, side="right")

        # wrap sidebar content in a scrollable frame (attach to .body)
        self.right_scroll = ScrollableFrame(self.right_sidebar.body)
        self.right_scroll.pack(fill="both", expand=True)

        # put panels inside the scrollable body (stacked)
        self.faces_viewer = FacesFrame(self.right_scroll.body, None, self.db)
        self.faces_viewer.pack(fill="x", padx=5, pady=5)

        self.exif_viewer = ExifViewer(self.right_scroll.body, self.db)
        self.exif_viewer.pack(fill="x", padx=5, pady=5)

        self.score_viewer = ScoreViewer(self.right_scroll.body, self.db)
        self.score_viewer.pack(fill="x", padx=5, pady=5)

        self.duplicate_viewer = DuplicateViewer(self.right_scroll.body, self.db)
        self.duplicate_viewer.pack(fill="x", padx=5, pady=5)

        # filmstrip stays at bottom of the main window
        self.filmstrip = FilmstripViewer(
            self,
            self.photo_viewer,
            exif_viewer=self.exif_viewer,
            score_viewer=self.score_viewer,
        )
        self.filmstrip.pack(fill="x", side="bottom")

        # ---------- Debounced layout update ----------
        self._layout_after_id = None
        self.bind("<Configure>", self._on_configure)

        # ---------- Set default active viewer last ----------
        self._switch_to_photos()

    # ---------- Configure handler ----------
    def _on_configure(self, event):
        if self._layout_after_id:
            self.after_cancel(self._layout_after_id)
        self._layout_after_id = self.after(100, self.update_layout)

    # ---------- Go Back Logic --------------
    def go_back(self):
        if hasattr(self, "prev_viewer") and self.prev_viewer:
            if self.active_viewer:
                self.active_viewer.place_forget()
            self.active_viewer = self.prev_viewer
            self.update_layout()

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
        self.left_sidebar.toggle_btn.config(
            text="⮞" if self.left_sidebar.collapsed else "⮜"
        )
        self.right_sidebar.toggle_btn.config(
            text="⮜" if self.right_sidebar.collapsed else "⮞"
        )

        # Show/hide and place Back button depending on active view
        if isinstance(self.active_viewer, SinglePhotoViewer):
            self.back_btn.place(x=lw + 10, y=10)
            self.back_btn.lift() 
        else:
            self.back_btn.place_forget()

    # ---------- Menubar ----------
    def setup_menubar(self):
        menubar = ttk.Menu(self)

        # File
        file_menu = ttk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Collection", command=lambda: print("New Collection"))
        file_menu.add_command(label="Open Collection...", command=lambda: print("Open"))
        file_menu.add_separator()
        file_menu.add_command(label="Import Photos", command=self.sidebar_import_photos)
        file_menu.add_command(label="Export Selection", command=lambda: print("Export"))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit
        edit_menu = ttk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Preferences", command=lambda: print("Preferences"))
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Collections
        collections_menu = ttk.Menu(menubar, tearoff=0)
        collections_menu.add_command(label="View Photos", command=self._switch_to_photos)
        collections_menu.add_command(label="View Collections", command=self._switch_to_collections)
        menubar.add_cascade(label="Collections", menu=collections_menu)

        self.config(menu=menubar)

    # ---------- Import wrapper ----------
    def sidebar_import_photos(self):
        self.sidebar_buttons.import_files()

    # ---------- Switch view helpers ----------
    def _switch_to_photos(self):
        self.prev_viewer = self.active_viewer
        if self.active_viewer:
            self.active_viewer.place_forget()
        self.active_viewer = self.photo_viewer
        self.back_btn.place_forget()  # hide if visible
        self.update_layout()

    def _switch_to_collections(self):
        self.prev_viewer = self.active_viewer
        if self.active_viewer:
            self.active_viewer.place_forget()
        self.active_viewer = self.collections_viewer
        self.back_btn.place_forget()  # hide if visible
        self.collections_viewer.refresh_collections()
        self.update_layout()

    # ---------- NEW: open single image in full center pane ----------
    def open_single_view(self, photo_path: str):
        self.prev_viewer = self.active_viewer
        if self.active_viewer:
            self.active_viewer.place_forget()
        self.single_viewer = SinglePhotoViewer(self, photo_path=photo_path)
        self.active_viewer = self.single_viewer
        self.update_layout()

    # ---------- NEW: centered info dialog for pop-ups ----------
    def show_centered_info(self, title: str, message: str):
        """Show a simple OK dialog centered over the main window."""
        win = tk.Toplevel(self)
        win.title(title)
        win.transient(self)
        win.grab_set()
        win.resizable(False, False)

        frm = ttk.Frame(win, padding=16)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text=message).pack(pady=(0, 12))
        ttk.Button(frm, text="OK", command=win.destroy).pack()

        # center on the app window
        self.update_idletasks()
        w, h = 320, 140
        x = self.winfo_rootx() + (self.winfo_width() - w) // 2
        y = self.winfo_rooty() + (self.winfo_height() - h) // 2
        win.geometry(f"{w}x{h}+{x}+{y}")


# ---------- Helpers ----------
def resource_path(filename: str) -> str:
    base = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    return os.path.join(base, filename)


def center_window(window, width, height):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


# ---------- Splash screen as Toplevel over the (hidden) main window ----------
def create_splash(master):
    """
    Create a borderless splash Toplevel on top of the hidden main window.
    """
    splash = tk.Toplevel(master)
    splash.title("Loading AutoCull…")
    splash.resizable(False, False)
    splash.overrideredirect(True)

    W, H = 560, 340
    center_window(splash, W, H)

    container = ttk.Frame(splash, padding=16)
    container.pack(fill="both", expand=True)

    logo_path = resource_path("logo/autocull_logo.webp")
    try:
        if not _HAS_PIL:
            raise RuntimeError("Pillow not installed; required for .webp")
        im = Image.open(logo_path).convert("RGBA")
        im.thumbnail((W - 64, H - 120), Image.LANCZOS)
        img_obj = ImageTk.PhotoImage(im)
        img_lbl = ttk.Label(container, image=img_obj)
        img_lbl.image = img_obj  # prevent GC
        img_lbl.pack(pady=(12, 12))
    except Exception as e:
        ttk.Label(container, text="AutoCull", font=("Segoe UI", 24, "bold")).pack(pady=(32, 8))
        ttk.Label(container, text=f"Loading… (logo error: {e})").pack(pady=(0, 12))

    ttk.Label(container, text="Loading…", font=("Segoe UI", 11)).pack()
    return splash


if __name__ == "__main__":
    # 1) Create the main app (this creates the single Tk root)
    app = AutoCullApp()
    app.withdraw()  # keep it hidden while splash shows
    center_window(app, 1200, 800)

    # 2) Create splash as a Toplevel over the hidden app
    splash = create_splash(app)

    # 3) After delay, close splash and show the app
    def _reveal():
        try:
            splash.destroy()
        except Exception:
            pass
        app.deiconify()

    splash.after(2000, _reveal)

    # 4) Run the single mainloop on the app (not on the splash)
    app.mainloop()
