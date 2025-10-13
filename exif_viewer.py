from base_sidebar_viewer import BaseSidebarViewer

class ExifViewer(BaseSidebarViewer):
    """
    A class that inherits from BaseSidebarViewer to display EXIF data
    in a sidebar view.

    Attributes:
        parent: The parent widget.
        db: Database connection object.
    """

    def __init__(self, parent, db, **kwargs):
        """
        Initialize the ExifViewer instance.

        Args:
            parent: The parent widget.
            db: Database connection object.
            **kwargs: Additional keyword arguments to pass to BaseSidebarViewer.
        """
        super().__init__(
            parent,
            db,
            title="EXIF Data",  # Title of the sidebar view
            default_height=400,  # Default height of the sidebar
            **kwargs
        )

    def setup_columns(self, tree):
        """
        Setup the columns for the Treeview widget.

        Args:
            tree: The tk.Treeview widget to be configured.
        """
        # Define the column names
        tree["columns"] = ("tag", "value")

        # Set headings for each column with display text
        tree.heading("tag", text="Tag")
        tree.heading("value", text="Value")

        # Configure column widths and anchor alignment (west/left)
        tree.column("tag", width=150, anchor="w")
        tree.column("value", width=250, anchor="w")

    def update_content(self, photo_id):
        """
        Update the content of the sidebar view with EXIF data for a given photo ID.

        Args:
            photo_id: The ID of the photo to get EXIF data for.
        """
        # Clear any existing items in the tree
        self.clear_tree()

        if not photo_id:
            return

        # Get EXIF data from database for the specified photo_id
        exif = self.db.get_exif(photo_id)

        if not exif:
            return

        # Populate the tree with EXIF data
        for key, value in exif.items():
            # If value is a list or tuple, convert it to a comma-separated string
            if isinstance(value, (list, tuple)):
                value = ", ".join(str(v) for v in value)

            # Insert a row into the tree with tag and formatted value
            self.tree.insert("", "end", values=(key, str(value)))