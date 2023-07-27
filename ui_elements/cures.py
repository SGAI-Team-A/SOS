import tkinter as tk

class CureCounter(object):
    def __init__(self, root, scorekeeper, x, y):
        self.cure_counter = tk.Canvas(
            root,
            background='white',
            borderwidth=1,
            relief="flat",
            width=200,
            height=60
        )
        self.scorekeeper = scorekeeper
        self.x = x
        self.y = y
        self.text = tk.Label(self.cure_counter, font=("Arial", 15), bg="white")
    
    def build(self):
        self.cure_counter.place(x=self.x, y=self.y)
        self.update_text()
        self.text.place(relx=0.5, rely=0.5, anchor="center")
    
    def update_text(self):
        self.text.config(text="Cures: {}".format(self.scorekeeper.get_cures()))