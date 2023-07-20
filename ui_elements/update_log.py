import tkinter as tk

class UpdateLog(tk.Frame):
    def __init__(self, update, canvas):
        self.canvas = canvas
        self.canvas.delete("all")
        if not update == "":
            self.canvas.create_text(350, 50, text = update, fill = "black", font = ('Times 10'))
        self.canvas.pack()