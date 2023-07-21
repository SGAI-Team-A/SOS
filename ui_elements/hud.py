import tkinter as tk
import os
from PIL import ImageTk, Image

class HUD():
    def __init__(self, root, w, h):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'post-render.png')
        ambulance = ImageTk.PhotoImage(Image.open(path).convert("RGBA").resize((w, h), Image.LANCZOS))
        label = tk.Label(root, image=ambulance)
        label.image = ambulance
        label.pack()
        # label.grid(row=0, column=0)
