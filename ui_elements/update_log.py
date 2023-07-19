import tkinter as tk

class UpdateLog(tk.Frame):
    def __init__(self, update, canvas):
        self.canvas = canvas
        text = update
        self.canvas.delete("all")
        if not text == "":
            self.canvas.create_text(250, 50, text=text, fill="black", font=('Helvetica 10'), tag = "a")
        self.canvas.pack()