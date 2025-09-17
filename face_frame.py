import tkinter as tk
from PIL import ImageTk
from PIL import Image

class FaceFrame(tk.Frame):
    """
    A Tkinter Frame that displays a cropped face from an image.
    Attributes:
        photo_path (str): The path to the image file.
        bounding_box (tuple): A tuple defining the bounding box (left, upper, right, lower).
    Author:
        Daniel Paxton
    """
    def __init__(self, parent, photo_path, bounding_box):

        # Initialize the parent class
        super().__init__(parent)

        # Store the photo path and bounding box 
        self.photo_path = photo_path
        self.bounding_box = bounding_box

        # Load and crop the image
        self.image = self.crop_face()

        # create a PhotoImage object
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.label = tk.Label(self, image=self.photo_image)

        self.label.pack()
    
    def crop_face(self):
        """
        Crops the region of the image defined by the bounding box.

        Returns:
            PIL.Image: The cropped image.
        """
        image = Image.open(self.photo_path)
        cropped_image = image.crop(self.bounding_box) # (left, upper, right, lower)
        return cropped_image