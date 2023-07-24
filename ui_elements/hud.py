import tkinter as tk
from PIL import Image, ImageTk
import os

class HUD():
    def __init__(self, root, w, h):
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'post-render.png')
        self.ambulance = ImageTk.PhotoImage(Image.open(self.path).resize((w, h), Image.LANCZOS))

    def build_hud(self, root):
        self.delete_img(root)
        root.create_image(0, 0, anchor=tk.NW, image=self.ambulance, tags='hud')

    def delete_img(self, root):
        root.delete('hud')

    def get_hud(self):
        return self.ambulance


