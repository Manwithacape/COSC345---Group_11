# progress_dialog.py
import ttkbootstrap as ttk
import tkinter as tk

class ProgressDialog(tk.Toplevel):
    def __init__(self, master, title="Working...", message="Please wait...",
                 indeterminate=True, maximum=100):
        super().__init__(master)
        self.title(title)
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()

        self.indeterminate = indeterminate
        self.maximum = maximum

        frm = ttk.Frame(self, padding=20)
        frm.pack(fill="both", expand=True)

        self._label = ttk.Label(frm, text=message, font=("Segoe UI", 11))
        self._label.pack(pady=(0, 10))

        # use ttk.Progressbar from ttkbootstrap
        self.progress = ttk.Progressbar(
            frm,
            mode="indeterminate" if indeterminate else "determinate",
            maximum=self.maximum
        )
        self.progress.pack(fill="x", pady=(0, 10))

        # start indeterminate animation if requested
        if indeterminate:
            try:
                self.progress.start(10)
            except Exception:
                # some platforms may throw if start is called too early; ignore
                pass

        # Prevent user from closing the dialog by clicking the window close button
        self.protocol("WM_DELETE_WINDOW", lambda: None)

        # Center on parent safely (guard against masters not yet mapped)
        try:
            self.update_idletasks()
            x = master.winfo_rootx() + (master.winfo_width() // 2 - self.winfo_width() // 2)
            y = master.winfo_rooty() + (master.winfo_height() // 2 - self.winfo_height() // 2)
            self.geometry(f"+{x}+{y}")
        except Exception:
            pass

    def start(self, interval=10):
        """Switch to indeterminate mode and start the animation.
        Safe to call even if already indeterminate."""
        self.indeterminate = True
        try:
            self.progress.config(mode="indeterminate")
            self.progress.start(interval)
            self.update_idletasks()
        except Exception:
            pass

    def set_progress(self, value, maximum=None):
        """Switch to determinate mode and set value."""
        if maximum is not None:
            self.maximum = maximum
            self.progress.config(maximum=self.maximum)
        self.indeterminate = False
        try:
            self.progress.config(mode="determinate")
            self.progress["value"] = value
            self.update_idletasks()
        except Exception:
            pass

    def set_message(self, message):
        """Update the text shown above the progress bar."""
        try:
            self._label.config(text=message)
            self.update_idletasks()
        except Exception:
            pass

    def finish(self, success=True, imported_count=None, error=None, delay=200):
        """Stop animation and close the dialog.

        - success: bool (unused by caller in your code, but available)
        - imported_count / error: optional extras we briefly display
        - delay: milliseconds to wait before destroying so user can see final message
        """
        try:
            # stop any running indeterminate animation
            try:
                self.progress.stop()
            except Exception:
                pass

            # if determinate, show full progress
            if not self.indeterminate:
                try:
                    self.progress["value"] = self.maximum
                except Exception:
                    pass

            # optionally display a final short message
            if success and imported_count is not None:
                try:
                    self._label.config(text=f"Completed: {imported_count} items")
                    self.update_idletasks()
                except Exception:
                    pass
            elif not success and error is not None:
                try:
                    self._label.config(text=f"Error: {error}")
                    self.update_idletasks()
                except Exception:
                    pass

            # destroy after small pause so user can see the final state
            self.after(delay, self.destroy)
        except Exception:
            # best-effort destroy
            try:
                self.destroy()
            except Exception:
                pass
