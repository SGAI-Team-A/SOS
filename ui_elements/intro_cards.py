import os
import tkinter as tk
from PIL import Image, ImageTk


class IntroCards(object):
    def __init__(self, root, w, h, destroy_callback, ui):
        self.root_ = tk.Canvas(root, width=w, height=h)
        self.root_.place(x=0, y=0)
        self.width = w
        self.height = h

        self.destroy_callback = destroy_callback

        self.image_paths = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'info-card.png'),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'info-card-2.png')
        ]
        self.ui = ui
        self.current_id = 0
        self.path = self.image_paths[self.current_id]
        self.build()
        self.root_.bind("<Button-1>", lambda e: self.show_next())
        
    def build(self):
        self.info_card = ImageTk.PhotoImage(Image.open(self.path).resize((self.width, self.height), Image.LANCZOS))
        self.image = self.root_.create_image(0, 0, anchor=tk.NW, image=self.info_card, tags='info_card')

    def show_next(self):
        self.current_id += 1
        if self.current_id == len(self.image_paths)-1:
            self.var = tk.IntVar()
            self.c1 = tk.Checkbutton(self.ui.root, text='real time', variable=self.var, onvalue=1, offvalue=0, command=self.selection)
            self.c1.pack()
            self.c1.place(x=1180, y=80)
            
        if self.current_id >= len(self.image_paths):
            self.root_.unbind("<Button-1>")
            self.root_.destroy()
            self.c1.destroy()
            self.destroy_callback()
        else:
            self.path = self.image_paths[self.current_id]
            self.build()
            
    def selection(self):
        if self.var.get() == 1:
            self.ui.set_real_time(True)
        else:
            self.ui.set_real_time(False)
