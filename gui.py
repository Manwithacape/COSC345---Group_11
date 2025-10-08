# gui.py
import ttkbootstrap as ttk
from sidebar_buttons import SidebarButtons

MIN_COLLAPSED = 30
MAX_WIDTH = 500
DEFAULT_WIDTH = 220
GRIP_WIDTH = 6


class Sidebar(ttk.Frame):
    def __init__(
        self,
        master,
        side="left",
        width=DEFAULT_WIDTH,
        db=None,
        photo_viewer=None,
        importer=None,
        **kwargs
    ):
        super().__init__(master, width=width, **kwargs)
        # self.config(borderwidth=2, relief="solid")
        self.master = master
        self.side = side
        self.width = width
        self.collapsed = False
        # Toolbar
        self.toolbar = ttk.Frame(self)
        self.toolbar.pack(fill="x")
        # ***** NEW: body container — put ALL sidebar content into this *****
        self.body = ttk.Frame(self)
        self.body.pack(fill="both", expand=True)
        # ***************************************************************
        if side == "left":
            self.toggle_btn = ttk.Button(
                self.toolbar,
                text="⮜",
                width=2,
                command=self.toggle,
                bootstyle="secondary",
            )
            self.toggle_btn.pack(side="right", padx=4, pady=4)
            self.grip = ttk.Frame(self, cursor="sb_h_double_arrow", width=GRIP_WIDTH)
            self.grip.pack(side="right", fill="y")
            # Add a vertical frame as a right border
            self.right_border = ttk.Frame(self, width=2, bootstyle="secondary")
            self.right_border.pack(side="right", fill="y")
        else:
            self.toggle_btn = ttk.Button(
                self.toolbar,
                text="⮞",
                width=2,
                command=self.toggle,
                bootstyle="secondary",
            )
            self.toggle_btn.pack(side="left", padx=4, pady=4)
            self.grip = ttk.Frame(self, cursor="sb_h_double_arrow", width=GRIP_WIDTH)
            self.grip.pack(side="left", fill="y")
        # Bind resize events
        self.grip.bind("<ButtonPress-1>", self._start_resize)
        self.grip.bind("<B1-Motion>", self._do_resize)

    # ----------------- Toggle -----------------
    def toggle(self):
        self.collapsed = not self.collapsed
        # Hide/show ONLY the body container; everything inside disappears/returns
        if self.collapsed:
            self.body.pack_forget()
        else:
            self.body.pack(fill="both", expand=True)
        self.master.update_layout()

    # ----------------- Resize -----------------
    def _start_resize(self, event):
        self._start_x = self.grip.winfo_rootx()
        self._start_width = self.width
        if self.collapsed:
            self.collapsed = False

    def _do_resize(self, event):
        mouse_x = self.grip.winfo_pointerx()
        delta = (
            mouse_x - self._start_x if self.side == "left" else self._start_x - mouse_x
        )
        self.width = max(MIN_COLLAPSED, min(MAX_WIDTH, self._start_width + delta))
        self.master.update_layout()
