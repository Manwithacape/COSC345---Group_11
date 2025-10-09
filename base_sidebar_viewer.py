"""
Defines a base class for sidebar viewers with collapsible headers,
scrollable treeviews, and a resizable grip.
"""

import ttkbootstrap as ttk
from db import Database

MIN_COLLAPSED_HEIGHT = 30
DEFAULT_HEIGHT = 300
GRIP_HEIGHT = 6


class BaseSidebarViewer(  # pylint: disable=too-many-ancestors, too-many-instance-attributes
    ttk.Frame
):
    """
    Base class for right-hand sidebar viewers.

    Provides:
      - Collapsible header bar
      - Scrollable Treeview
      - Resize grip

    Subclasses should:
      - Define self.title
      - Override setup_columns(tree)
      - Override update_content(photo_id)
    """

    def __init__(
        self,
        parent,
        db: Database,
        title: str = "Viewer",
        default_height: int = DEFAULT_HEIGHT,
        **kwargs,
    ) -> None:
        """
        Initialize the sidebar viewer.

        Args:
            parent: Parent Tkinter/ttk widget.
            db: Database instance for data access.
            title: Title for the header bar.
            default_height: Default expanded height.
            **kwargs: Additional ttk.Frame parameters.
        """
        super().__init__(parent, **kwargs)
        self.db = db
        self.title = title
        self.collapsed = False
        self.expanded_height = default_height

        # Predeclare resize handler state to avoid attribute-defined-outside-init
        self._start_y = 0
        self._start_height = default_height

        self.pack_propagate(False)
        self.configure(height=self.expanded_height)

        # ---------- Header ----------
        self.top_bar = ttk.Frame(self)
        self.top_bar.pack(fill="x")

        self.toggle_btn = ttk.Button(
            self.top_bar,
            text=f"{self.title} ⯆",
            bootstyle="secondary",
            command=self.toggle,
        )
        self.toggle_btn.pack(pady=0, padx=0, fill="x", anchor="w")

        # ---------- Treeview ----------
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(fill="both", expand=True)

        self.tree_scroll = ttk.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side="right", fill="y")

        self.tree = ttk.Treeview(
            self.tree_frame, show="headings", yscrollcommand=self.tree_scroll.set
        )
        self.setup_columns(self.tree)
        self.tree.pack(fill="both", expand=True)
        self.tree_scroll.config(command=self.tree.yview)

        # ---------- Style ----------
        # Theme handles styling

        # ---------- Resize Grip ----------
        self.grip = ttk.Frame(self, cursor="sb_v_double_arrow", height=GRIP_HEIGHT)
        self.grip.pack(fill="x", side="bottom")
        self.grip.bind("<ButtonPress-1>", self._start_resize)
        self.grip.bind("<B1-Motion>", self._do_resize)

    # ----------------- Must Override -----------------
    def setup_columns(self, tree: ttk.Treeview) -> None:
        """Define Treeview columns in subclass."""
        raise NotImplementedError

    def update_content(self, photo_id) -> None:  # type: ignore[override]
        """Populate tree with rows in subclass."""
        raise NotImplementedError

    # ----------------- Toggle -----------------
    def toggle(self) -> None:
        """Collapse/expand the viewer and update header text."""
        if self.collapsed:
            self.configure(height=self.expanded_height)
            self.tree_frame.pack(fill="both", expand=True)
            self.grip.pack(fill="x", side="bottom")
            self.toggle_btn.config(text=f"{self.title} ⯆")
            self.collapsed = False
        else:
            self.expanded_height = self.winfo_height()
            self.tree_frame.pack_forget()
            self.grip.pack_forget()
            self.configure(height=MIN_COLLAPSED_HEIGHT)
            self.toggle_btn.config(text=f"{self.title}⯈")
            self.collapsed = True

    # ----------------- Resize -----------------
    def _start_resize(self, _event) -> None:
        """Begin drag-resize: capture starting mouse Y and current height."""
        self._start_y = self.grip.winfo_rooty()
        self._start_height = self.winfo_height()
        if self.collapsed:
            self.toggle()

    def _do_resize(self, _event) -> None:
        """Resize the viewer height as the mouse is dragged."""
        mouse_y = self.grip.winfo_pointery()
        delta = mouse_y - self._start_y
        new_height = max(MIN_COLLAPSED_HEIGHT, self._start_height + delta)
        self.expanded_height = new_height
        self.configure(height=new_height)

    # ----------------- Helpers -----------------
    def clear_tree(self) -> None:
        """Remove all rows from the Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)
