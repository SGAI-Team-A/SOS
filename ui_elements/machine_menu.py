import tkinter as tk


class MachineMenu(object):
    def __init__(self, root, items):
        self.canvas = tk.Canvas(root, width=500, height=80)
        self.canvas.place(x=450, y=720)
        self.buttons = create_buttons(self.canvas, items)
        create_menu(self.buttons)


def create_buttons(canvas, items):
    buttons = []
    for item in items:
        (text, action) = item
        buttons.append(tk.Button(canvas, text=text, height=2, width=15,
                                 command=action))
    return buttons


def create_menu(buttons):
    for button in buttons:
        button.pack(side=tk.LEFT, padx=10)
