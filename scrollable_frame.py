# scrollable_frame.py

import tkinter as tk
import ttkbootstrap as ttk

class ScrollableFrame(ttk.Frame):
    """A simple vertically scrollable frame for stacking widgets."""

    def __init__(self, parent, **kwargs):
        """
        Initialize the ScrollableFrame.

        Args:
            parent: The parent widget.
            **kwargs: Additional keyword arguments to pass to ttk.Frame.
        """
        super().__init__(parent, **kwargs)

        # Create a canvas for scrolling
        self.canvas = tk.Canvas(self, highlightthickness=0)

        # Create vertical scrollbar and configure it with the canvas
        self.vbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vbar.set)

        # Pack widgets into the frame
        self.vbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create a frame inside the canvas to hold content
        self.body = ttk.Frame(self.canvas)
        self._win = self.canvas.create_window((0, 0), window=self.body, anchor="nw")

        # Bind events for resizing and scrolling
        self.body.bind("<Configure>", self._on_body_configure)  # Resize event
        self.canvas.bind("<Configure>", self._on_canvas_configure)  # Canvas resize

        # Bind mouse events for scroll wheel support
        self.body.bind("<Enter>", self._bind_mouse)
        self.body.bind("<Leave>", self._unbind_mouse)

    def _on_body_configure(self, _):
        """
        Update the canvas scroll region when the body frame is configured.

        Args:
            _: Event object (unused).
        """
        # Configure the scrollregion to match the content size
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, _):
        """
        Adjust window width when canvas is resized.

        Args:
            _: Event object (unused).
        """
        # Update the width of the window item in the canvas to match canvas width
        self.canvas.itemconfigure(self._win, width=self.canvas.winfo_width())

    def _on_mousewheel(self, event):
        """
        Handle mouse wheel events for scrolling.

        Args:
            event: The event object containing mouse wheel information.
        """
        if event.num == 4:  # Linux up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux down
            self.canvas.yview_scroll(1, "units")
        else:  # Windows / macOS
            # Calculate scroll units based on delta (platform-dependent)
            self.canvas.yview_scroll(int(-event.delta / 120), "units")

    def _bind_mouse(self, _):
        """
        Bind mouse wheel events to the canvas.

        Args:
            _: Event object (unused).
        """
        # Bind scroll events for all platforms
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)  # Linux forward button
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)  # Linux backward button

    def _unbind_mouse(self, _):
        """
        Unbind mouse wheel events from the canvas.

        Args:
            _: Event object (unused).
        """
        # Unbind scroll events for all platforms
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")
