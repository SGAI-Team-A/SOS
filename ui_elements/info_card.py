import tkinter as tk
import os
from PIL import ImageTk, Image

class InfoCard(object):
    def __init__(self, root, w, h):
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'info-card.png')
        self.info_card = ImageTk.PhotoImage(Image.open(self.path).resize((w,h), Image.LANCZOS))
        self.root_ = tk.Canvas(root, width=w, height=h)
        self.root_.place(x=0,y=0)
        self.build(self.root_)
    
    def build(self, canvas):
        self.image = canvas.create_image(0, 0, anchor=tk.NW, image=self.info_card, tags='info_card')