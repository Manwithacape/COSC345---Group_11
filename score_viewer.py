from base_sidebar_viewer import BaseSidebarViewer

class ScoreViewer(BaseSidebarViewer):
    """
    A class that extends BaseSidebarViewer to display photo scores in a sidebar.
    """

    def __init__(self, parent, db, **kwargs):
        """
        Initialize the ScoreViewer with a parent widget and database connection.

        Args:
            parent: The parent widget for this viewer.
            db: Database connection object.
            **kwargs: Additional keyword arguments to pass to the parent class.
        """
        # Call the constructor of the parent class with specified parameters
        super().__init__(parent, db, title="Photo Scores", default_height=300, **kwargs)

    def setup_columns(self, tree):
        """
        Set up columns for the treeview widget.

        Args:
            tree: The ttk.Treeview widget to set up.
        """
        # Define the columns and their headings
        tree["columns"] = ("metric", "value")
        tree.heading("metric", text="Metric")  # Set heading for 'metric' column
        tree.heading("value", text="Value")    # Set heading for 'value' column

        # Set column widths and alignment
        tree.column("metric", width=150, anchor="w")
        tree.column("value", width=150, anchor="w")

    def update_content(self, photo_id):
        """
        Update the content of the viewer with scores for a specific photo.

        Args:
            photo_id: The ID of the photo to get scores for.
        """
        # Clear existing content in the treeview
        self.clear_tree()

        # If no photo ID is provided, return early
        if not photo_id:
            return

        # Get scores for the given photo from the database
        scores = self.db.get_scores(photo_id)

        # If no scores are found, return early
        if not scores:
            return

        # Populate the treeview with score data
        for score in scores:
            # Insert a new row in the treeview with the score type and value
            self.tree.insert("", "end", values=(score["type"], str(score["value"])))
