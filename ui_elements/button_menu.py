import tkinter as tk
import os
from PIL import ImageTk, Image
from gameplay.enums import ActionCost
from ui_elements.button import Button

class ButtonMenu(object):
    def __init__(self, buttons: [str, Button]):
        self.buttons: dict[str: Button] = buttons

    # define if buttons are interactive (react at all) or not
    def set_interactive(self, interactive=False):
        for button in self.buttons.values():
            button.set_interactive(interactive)


    def disable_buttons(self, remaining_time, remaining_humanoids, at_capacity):
        if at_capacity:
            self.buttons["save"].set_disabled(True)
            self.buttons["skip"].set_disabled(True)
            self.buttons["squish"].set_disabled(True)
        else:
            self.buttons["save"].set_disabled(False)
            self.buttons["skip"].set_disabled(False)
            self.buttons["squish"].set_disabled(False)

        # Game over - no more buttons
        if remaining_humanoids == 0 or remaining_time <= 0:
            for button in self.buttons.values():
                button.set_disabled(True)
                button.set_interactive(False)
        #  Not enough time left? Disable action
        if (remaining_time - ActionCost.SCRAM.value) < ActionCost.SKIP.value:
            self.buttons['skip'].set_disabled(True)
        if (remaining_time - ActionCost.SCRAM.value) < ActionCost.SQUISH.value:
            self.buttons['squish'].set_disabled(True)
        if (remaining_time - ActionCost.SCRAM.value) < ActionCost.SAVE.value:
            self.buttons['save'].set_disabled(True)

