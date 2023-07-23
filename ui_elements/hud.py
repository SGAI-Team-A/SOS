import tkinter as tk
from PIL import Image, ImageTk
import os

class HUD():
    def __init__(self, root, w, h):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'post-render.png')
        self.ambulance = ImageTk.PhotoImage(Image.open(path).resize((w, h), Image.LANCZOS))
        root.create_image(0, 0, anchor=tk.NW, image=self.ambulance)


