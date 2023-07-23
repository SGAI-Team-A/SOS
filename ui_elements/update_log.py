import tkinter as tk

class UpdateLog(object):
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=700, height=100)
        self.canvas.place(x=120, y=40)
        self.canvas.delete("all")

    def set_update(self, update):
        self.canvas.delete("all")
        if not update == "":
            self.canvas.create_text(350, 50, text = update, fill = "black", font = ('Times 10'))