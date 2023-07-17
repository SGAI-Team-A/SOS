import tkinter as tk
import os
from PIL import ImageTk, Image

from gameplay.enums import ActionCost


class ButtonMenu(object):
    def __init__(self, root, items):
        self.canvas = tk.Canvas(root, width=500, height=80)
        self.canvas.place(x=100, y=150)
        self.buttons = create_buttons(self.canvas, items)
        create_menu(self.buttons)

    def disable_buttons(self, remaining_time, remaining_humanoids, at_capacity):
        if remaining_humanoids == 0 or remaining_time <= 0:
            for i in range(0, len(self.buttons)):
                self.buttons[i].config(state="disabled")
        #  Not enough time left? Disable action
        if (remaining_time - ActionCost.SCRAM.value) < ActionCost.SKIP.value:
            self.buttons[0].config(state="disabled")
        if (remaining_time - ActionCost.SCRAM.value) < ActionCost.SQUISH.value:
            self.buttons[1].config(state="disabled")
        if (remaining_time - ActionCost.SCRAM.value) < ActionCost.SAVE.value:
            self.buttons[2].config(state="disabled")
        if at_capacity:
            self.buttons[0].config(state="disabled")
            self.buttons[1].config(state="disabled")
            self.buttons[2].config(state="disabled")


def create_buttons(canvas, items):
    buttons = []
    for item in items:
        (text, action) = item
        buttons.append(tk.Button(canvas, text=text, height=2, width=15,
                                 command=action))
    return buttons


def create_menu(buttons):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'logo.png')
    logo = ImageTk.PhotoImage(Image.open(path).resize((300, 50), Image.LANCZOS))
    label = tk.Label(image=logo)
    label.image = logo

    # Position image
    label.place(x=10, y=10)

    for button in buttons:
        button.pack(side=tk.TOP, pady=10)
