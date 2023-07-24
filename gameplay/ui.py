import math
import tkinter as tk

from ui_elements.button import Button
from ui_elements.button_menu import ButtonMenu
from ui_elements.capacity_meter import CapacityMeter
from ui_elements.clock import Clock
from endpoints.machine_interface import MachineInterface
from ui_elements.game_viewer import GameViewer
from ui_elements.machine_menu import MachineMenu
from os.path import join
from ui_elements.update_log import UpdateLog


class UI(object):
    def __init__(self, data_parser, scorekeeper, data_fp, is_disable):
        #  Base window setup
        w, h = 1280, 720
        self.root = tk.Tk()
        self.root.title("Beaverworks SGAI 2023 - Dead or Alive")
        self.root.geometry(str(w) + 'x' + str(h))
        self.root.resizable(False, False)

        self.frame = tk.Canvas(self.root, width=w, height=h)
        self.frame.place(x=0, y=0)

        self.humanoid = data_parser.get_random()
        if not is_disable:
            self.machine_interface = MachineInterface(self.frame, w, h)

        #  Display the game
        self.game_viewer = GameViewer(self.frame, w, h, data_fp, self.humanoid, scorekeeper)
        self.root.bind("<Delete>", self.game_viewer.delete_photo)

        self.root.bind("<Button-1>", lambda e: print("x: {}, y: {}".format(e.x, e.y)))

        buttons = {
            'skip': Button(
                x=0,
                y=0,
                width=0,
                height=0,
                on_click=lambda: [scorekeeper.skip(self.humanoid),
                                  self.update_ui(scorekeeper),
                                  self.get_next(
                                      data_fp,
                                      data_parser,
                                      scorekeeper)]
            ),
            'squish': Button(
                x=0,
                y=0,
                width=0,
                height=0,
                on_click=lambda: [scorekeeper.squish(self.humanoid),
                                  self.update_ui(scorekeeper),
                                  self.get_next(
                                      data_fp,
                                      data_parser,
                                      scorekeeper)]
            ),
            'save': Button(
                x=0,
                y=0,
                width=0,
                height=0,
                on_click=lambda: [scorekeeper.save(self.humanoid),
                                  self.update_ui(scorekeeper),
                                  self.get_next(
                                      data_fp,
                                      data_parser,
                                      scorekeeper)]
            ),
            'scram': Button(
                x=0,
                y=0,
                width=0,
                height=0,
                on_click=lambda: [scorekeeper.scram(),
                                  self.update_ui(scorekeeper),
                                  self.get_next(
                                      data_fp,
                                      data_parser,
                                      scorekeeper)]
            ),
        }

        for button in buttons.values():
            self.root.bind("<Button-1>", button.callback, add="+")

        #  Add buttons and logo
        user_buttons = [("Skip", lambda: [scorekeeper.skip(self.humanoid),
                                          self.update_ui(scorekeeper),
                                          self.get_next(
                                              data_fp,
                                              data_parser,
                                              scorekeeper)]),
                        ("Squish", lambda: [scorekeeper.squish(self.humanoid),
                                            self.update_ui(scorekeeper),
                                            self.get_next(
                                                data_fp,
                                                data_parser,
                                                scorekeeper)]),
                        ("Save", lambda: [scorekeeper.save(self.humanoid),
                                          self.update_ui(scorekeeper),
                                          self.get_next(
                                              data_fp,
                                              data_parser,
                                              scorekeeper)]),
                        ("Scram", lambda: [scorekeeper.scram(),
                                           self.update_ui(scorekeeper),
                                           self.get_next(
                                               data_fp,
                                               data_parser,
                                               scorekeeper)])]
        self.button_menu = ButtonMenu(self.frame, user_buttons)

        # Display ambulance capacity
        self.capacity_meter = CapacityMeter(self.frame, w, h, data_parser.capacity)

        self.root.mainloop()

    def update_ui(self, scorekeeper):
        self.capacity_meter.update_fill(scorekeeper.get_current_capacity(), scorekeeper.get_last_saved())
        self.game_viewer.update_else()

    def on_resize(self, event):
        w, h = 0.6 * self.root.winfo_width(), 0.7 * self.root.winfo_height()
        self.game_viewer.canvas.config(width=w, height=h)

    def get_next(self, data_fp, data_parser, scorekeeper):
        remaining = len(data_parser.unvisited)

        # Ran out of humanoids? Disable skip/save/squish
        if remaining == 0 or scorekeeper.remaining_time <= 0:
            self.capacity_meter.update_fill(0, None)
            self.game_viewer.delete_photo(None)
            self.game_viewer.display_score(scorekeeper.get_score())
            self.button_menu.disable_buttons(scorekeeper.remaining_time, remaining, scorekeeper.at_capacity())
        else:
            humanoid = data_parser.get_random()
            # Update visual display
            self.humanoid = humanoid
            fp = join(data_fp, self.humanoid.fp)
            self.game_viewer.update(fp, self.humanoid)

        # Disable button(s) if options are no longer possible
        self.button_menu.disable_buttons(scorekeeper.remaining_time, remaining, scorekeeper.at_capacity())
