import tkinter as tk
class UpdateLog(object):
    def __init__(self, root):
        self.canvas = root
        self.canvas.delete("update_text")

    def set_update(self, update):
        self.canvas.delete("update_text")
        if not update == "":
            self.canvas.create_text(self.canvas.winfo_width()/2, 150, text = update, fill = "black", font = ('Times 10'), tags='update_text', anchor='center')
            self.canvas.tag_raise('update_text')