# main_viewer.py
import ttkbootstrap as ttk

class MainViewer(ttk.Frame):
    """
    Base scrollable viewer using a Canvas + Frame.
    Supports dynamic resizing and optional single-item display.
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.canvas = ttk.Canvas(self, highlightthickness=0)
        self.scrollbar_y = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.scrollbar_y.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = ttk.Frame(self.canvas)
        self.window_id = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Guard: don't let inner-frame updates fight single-photo mode
        self.inner_frame.bind("<Configure>", self._on_inner_configure)

        self.canvas.bind("<Configure>", self._on_resize)

        self.selected_idx = None
        self.single_item_active = False

    def _on_inner_configure(self, event=None):
        if self.single_item_active:
            return
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_resize(self, event=None):
        """Resize inner frame width to match canvas width (override if needed)."""
        if not self.canvas.winfo_exists():
            return
        # In single-photo mode, the single viewer manages its own sizing.
        if self.single_item_active:
            return
        self.canvas.itemconfig(self.window_id, width=self.canvas.winfo_width())
        self._reflow_grid()

    def _reflow_grid(self):
        """Override in subclass if grid layout is needed."""
        pass
