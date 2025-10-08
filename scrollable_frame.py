# scrollable_frame.py
import tkinter as tk
import ttkbootstrap as ttk


class ScrollableFrame(ttk.Frame):
    """A simple vertically scrollable frame for stacking widgets."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.vbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vbar.set)

        self.vbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.body = ttk.Frame(self.canvas)
        self._win = self.canvas.create_window((0, 0), window=self.body, anchor="nw")

        # resize/scroll plumbing
        self.body.bind("<Configure>", self._on_body_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # mouse-wheel scrolling
        self.body.bind("<Enter>", self._bind_mouse)
        self.body.bind("<Leave>", self._unbind_mouse)

    def _on_body_configure(self, _):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, _):
        self.canvas.itemconfigure(self._win, width=self.canvas.winfo_width())

    def _on_mousewheel(self, event):
        if event.num == 4:  # Linux up
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux down
            self.canvas.yview_scroll(1, "units")
        else:  # Windows / macOS
            self.canvas.yview_scroll(int(-event.delta / 120), "units")

    def _bind_mouse(self, _):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mouse(self, _):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")
