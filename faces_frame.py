import tkinter as tk
import ttkbootstrap as ttk
from face_frame import FaceFrame

class FacesFrame(tk.Frame):
    """
    A Tkinter Frame that displays multiple cropped faces from an image.
    Attributes:
        photo_path (str): The path to the image file.
        bounding_boxes (list): A list of tuples defining the bounding boxes [(left, upper, right, lower), ...].
    """
    def __init__(self, parent, photo_id, db):
        # Initialize the parent class
        super().__init__(parent)

        # Store the photo path and bounding boxes
        self.photo_id = photo_id
        self.db = db

        self.face_frames = []
        self.create_face_frames()

        self.toggled = True # Faces are shown by default
        
        # make a collapse/expand button
        self.toggle_btn = ttk.Button(
            self,
            text="Faces ⯆",
            command=self.toggle_faces,
            bootstyle="secondary"
        )
        self.toggle_btn.pack(side="top", pady=5, fill="x")

    def update_faces(self, photo_id):
        """
        Update the FacesFrame to display faces from the new photo_id.
        Clears existing faces and creates new FaceFrame instances.
        """
        self.photo_id = photo_id
        self.clear_faces()
        self.create_face_frames()

    def create_face_frames(self):
        """
        Create FaceFrame instances for each bounding box and pack them into the FacesFrame.
        """
        if not self.photo_id:
            return
        
        self.face_data = self.db.get_faces(self.photo_id) # x1, y1, x2, y2, photo_path
        photo_path = self.face_data[0]['file_path']
        bounding_boxes = [(face['x1'], face['y1'], face['x2'], face['y2']) for face in self.face_data]

        for bbox in bounding_boxes:
            face_frame = FaceFrame(self, photo_path, bbox)
            face_frame.pack(side="top", pady=5)
            self.face_frames.append(face_frame)

        self.show_faces()

    def clear_faces(self):
        """
        Clear all FaceFrame instances from the FacesFrame.
        """
        for face_frame in self.face_frames:
            face_frame.destroy()
        self.face_frames.clear()

    def hide_faces(self):
        """
        Hide all FaceFrame instances without destroying them.
        """
        for face_frame in self.face_frames:
            face_frame.pack_forget()

    def show_faces(self):
        """
        Show all FaceFrame instances that were previously hidden.
        """
        for face_frame in self.face_frames:
            face_frame.pack(side="top", pady=5)

    def toggle_faces(self):
        """
        Toggle the visibility of the FaceFrame instances.
        """
        if self.toggled:
            self.hide_faces()
            self.toggle_btn.config(text="Show Faces ⯈")
        else:
            self.show_faces()
            self.toggle_btn.config(text="Hide Faces ⯆")
        self.toggled = not self.toggled

        # Repack the toggle button to ensure it stays at the top
        self.toggle_btn.pack(side="top", pady=5)