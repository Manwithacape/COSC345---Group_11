from base_sidebar_viewer import BaseSidebarViewer

class DuplicateViewer(BaseSidebarViewer):
    """
    A class that extends BaseSidebarViewer to display duplicate photos.
    """

    def __init__(self, parent, db, **kwargs):
        """
        Initialize the DuplicateViewer.

        Args:
            parent: The parent widget.
            db: The database connection.
            **kwargs: Additional keyword arguments.
        """
        # Call the parent class's initializer with specific title and height
        super().__init__(parent, db, title="Duplicates", default_height=400, **kwargs)
        self.selected_photo_id = None  # Initialize selected photo ID to None

    def setup_columns(self, tree):
        """
        Set up columns for the treeview widget.

        Args:
            tree: The treeview widget.
        """
        tree["columns"] = ("group_id", "photo_id", "file_name")

        # Set column headings and properties
        tree.heading("group_id", text="Group ID")
        tree.heading("photo_id", text="Photo ID")
        tree.heading("file_name", text="File Name")

        tree.column("group_id", width=80, anchor="center")
        tree.column("photo_id", width=80, anchor="center")
        tree.column("file_name", width=250, anchor="w")

    def update_content(self, photo_id):
        """
        Update the content of the viewer based on the selected photo ID.

        Args:
            photo_id: The ID of the selected photo.
        """
        self.clear_tree()  # Clear existing treeview items
        self.selected_photo_id = photo_id

        if not photo_id:
            return  # Exit if no photo ID is provided

        groups = self.db.get_groups_for_photo(photo_id)  # Get groups for the photo
        if not groups:
            return  # Exit if no groups are found

        # Iterate through each group and add photos to treeview
        for g in groups:
            group_id = g["group_id"]
            for p in self.db.get_photos_in_group(group_id):
                # Insert photo details into the treeview
                self.tree.insert(
                    "", "end", values=(group_id, p["photo_id"], p["file_name"])
                )