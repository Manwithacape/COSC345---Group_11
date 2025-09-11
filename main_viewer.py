# main_viewer.py
import ttkbootstrap as ttk
from base_viewer import BaseThumbnailViewer

class MainViewer(ttk.Frame):
    """Reusable scrollable canvas+frame structure with scrollbar."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.canvas = ttk.Canvas(self, highlightthickness=0)
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.scrollbar_y.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = ttk.Frame(self.canvas)
        self.window_id = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Keep scroll region synced
        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        """Resize inner frame width to match canvas width (override if needed)."""
        self.canvas.itemconfig(self.window_id, width=self.canvas.winfo_width())
