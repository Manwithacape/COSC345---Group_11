# gui.py
import tkinter as tk
from sidebar_buttons import SidebarButtons

MIN_COLLAPSED = 30
MAX_WIDTH = 500
DEFAULT_WIDTH = 220
GRIP_WIDTH = 6

class Sidebar(tk.Frame):

    def __init__(self, master, side="left", width=DEFAULT_WIDTH,
                 db=None, photo_viewer=None, importer=None, **kwargs):
        super().__init__(master, width=width, **kwargs)
        self.master = master
        self.side = side
        self.width = width
        self.collapsed = False

        # Toolbar
        self.toolbar = tk.Frame(self, bg="#2f2f2f")
        self.toolbar.pack(fill="x")

        if side == "left":
            self.toggle_btn = tk.Button(self.toolbar, text="⮜", width=2, command=self.toggle)
            self.toggle_btn.pack(side="right", padx=4, pady=4)
            
            # Button handler
            self.buttons = SidebarButtons(master, db=db, photo_viewer=photo_viewer, importer=importer)

            # --- Import Button ---
            self.import_btn = tk.Button(self, text="Import Files", command=self.buttons.import_files)
            self.import_btn.pack(padx=10, pady=10, anchor="n")

            # --- Find Duplicates Button ---
            self.dup_btn = tk.Button(self, text="Find Duplicates", command=self.buttons.find_duplicates)
            self.dup_btn.pack(padx=10, pady=10, anchor="n")
            
            self.grip = tk.Frame(self, cursor="sb_h_double_arrow", bg="#454545", width=GRIP_WIDTH)
            self.grip.pack(side="right", fill="y")
        else:
            self.toggle_btn = tk.Button(self.toolbar, text="⮞", width=2, command=self.toggle)
            self.toggle_btn.pack(side="left", padx=4, pady=4)
            self.grip = tk.Frame(self, cursor="sb_h_double_arrow", bg="#454545", width=GRIP_WIDTH)
            self.grip.pack(side="left", fill="y")

        # Bind resize events
        self.grip.bind("<ButtonPress-1>", self._start_resize)
        self.grip.bind("<B1-Motion>", self._do_resize)

        

    # ----------------- Toggle -----------------
    def toggle(self):
        self.collapsed = not self.collapsed
        self.master.update_layout()

    # ----------------- Resize -----------------
    def _start_resize(self, event):
        self._start_x = self.grip.winfo_rootx()
        self._start_width = self.width
        if self.collapsed:
            self.collapsed = False

    def _do_resize(self, event):
        mouse_x = self.grip.winfo_pointerx()
        delta = mouse_x - self._start_x if self.side == "left" else self._start_x - mouse_x
        self.width = max(MIN_COLLAPSED, min(MAX_WIDTH, self._start_width + delta))
        self.master.update_layout()
