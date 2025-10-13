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
        master,       # Main application window or container frame
        side="left",  # Position of the sidebar ('left' or 'right')
        width=DEFAULT_WIDTH,  # Initial width of the sidebar
        db=None,      # Database connection (not used in this code)
        photo_viewer=None,    # Photo viewer component (not used in this code)
        importer=None,        # Importer component (not used in this code)
        **kwargs
    ):
        """Initialize Sidebar with specified parameters and setup layout"""
        super().__init__(master, width=width, **kwargs)

        self.master = master
        self.side = side
        self.width = width
        self.collapsed = False

        # Toolbar at the top of the sidebar for controls
        self.toolbar = ttk.Frame(self)
        self.toolbar.pack(fill="x")

        # Body container that holds all sidebar content
        self.body = ttk.Frame(self)
        self.body.pack(fill="both", expand=True)

        # Configure toggle button and grip based on side position (left or right)
        if side == "left":
            self.toggle_btn = ttk.Button(
                self.toolbar,
                text="⮜",
                width=2,
                command=self.toggle,  # Function to collapse/expand sidebar
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
                command=self.toggle,  # Function to collapse/expand sidebar
                bootstyle="secondary",
            )
            self.toggle_btn.pack(side="left", padx=4, pady=4)

            self.grip = ttk.Frame(self, cursor="sb_h_double_arrow", width=GRIP_WIDTH)
            self.grip.pack(side="left", fill="y")

        # Bind mouse events to grip for resizing functionality
        self.grip.bind("<ButtonPress-1>", self._start_resize)
        self.grip.bind("<B1-Motion>", self._do_resize)

    def toggle(self):
        """Toggle between collapsed and expanded states of the sidebar"""
        self.collapsed = not self.collapsed

        # Show/hide body container based on collapse state
        if self.collapsed:
            self.body.pack_forget()
        else:
            self.body.pack(fill="both", expand=True)

        # Update layout to reflect changes
        self.master.update_layout()

    def _start_resize(self, event):
        """Initialize resizing by recording start position and width"""
        self._start_x = self.grip.winfo_rootx()
        self._start_width = self.width

        if self.collapsed:
            self.collapsed = False  # Ensure sidebar is expanded during resize

    def _do_resize(self, event):
        """Resize the sidebar based on mouse movement"""
        mouse_x = self.grip.winfo_pointerx()

        # Calculate delta based on side position
        delta = (
            mouse_x - self._start_x if self.side == "left" else self._start_x - mouse_x
        )

        # Update width with constraints (minimum and maximum)
        self.width = max(MIN_COLLAPSED, min(MAX_WIDTH, self._start_width + delta))

        # Request layout update
        self.master.update_layout()
