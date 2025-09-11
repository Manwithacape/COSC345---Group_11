import ttkbootstrap as tb
import tkinter as tk

class CustomToolbar(tb.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.place(x=0, y=0, relwidth=1, height=40)  # No padding, fixed height

        # File Menubutton
        file_btn = tb.Menubutton(self, text="File", bootstyle="secondary")
        file_menu = tk.Menu(file_btn, tearoff=0)
        file_menu.add_command(label="New Collection", command=lambda: print("New Collection"))
        file_menu.add_command(label="Open Collection...", command=lambda: print("Open"))
        file_menu.add_separator()
        file_menu.add_command(label="Import Photos", command=parent.import_photos)
        file_menu.add_command(label="Export Selection", command=lambda: print("Export"))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=parent.quit)
        file_btn['menu'] = file_menu
        file_btn.place(x=0, y=0, width=80, height=40)  # No padding, fixed size

        # Edit Menubutton
        edit_btn = tb.Menubutton(self, text="Edit", bootstyle="secondary")
        edit_menu = tk.Menu(edit_btn, tearoff=0)
        edit_menu.add_command(label="Preferences", command=lambda: print("Preferences"))
        edit_btn['menu'] = edit_menu
        edit_btn.place(x=80, y=0, width=80, height=40)  # No padding, fixed size

        # Add more Menubuttons as needed
