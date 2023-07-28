import os
import tkinter as tk
from PIL import Image, ImageTk


class IntroCards(object):
    def __init__(self, root, w, h, destroy_callback):
        self.root_ = tk.Canvas(root, width=w, height=h)
        self.root_.place(x=0, y=0)
        self.width = w
        self.height = h

        self.destroy_callback = destroy_callback

        self.image_paths = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'info-card.png'),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'info-card-2.png')
        ]

        self.current_id = 0
        self.path = self.image_paths[self.current_id]
        self.build()

    def build(self):
        self.info_card = ImageTk.PhotoImage(Image.open(self.path).resize((self.width, self.height), Image.LANCZOS))
        self.image = self.root_.create_image(0, 0, anchor=tk.NW, image=self.info_card, tags='info_card')

    def show_next(self):
        self.current_id += 1
        if self.current_id >= len(self.image_paths):
            self.root_.destroy()
            self.destroy_callback()
        else:
            self.path = self.image_paths[self.current_id]
            self.build()
