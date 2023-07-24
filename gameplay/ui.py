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
        scale_factor = w / 1920  # original image size is 1920 by 1080
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

        # set up the buttons
        def on_disabled():
            self.game_viewer.update_log.set_update("Not enough time left!"),

        buttons = {
            'skip': Button(
                corners=[(1290, 682), (1574, 690), (1570, 844), (1286, 828) ],
                on_click=lambda: [scorekeeper.skip(self.humanoid),
                                  self.update_ui(scorekeeper),
                                  self.get_next(
                                      data_fp,
                                      data_parser,
                                      scorekeeper)],
                on_disabled_click=on_disabled,
                scale_factor=scale_factor
            ),
            'squish': Button(
                corners=[(1288, 840), (1566, 856), (1562, 1008), (1284, 986),],
                on_click=lambda: [scorekeeper.squish(self.humanoid),
                                  self.update_ui(scorekeeper),
                                  self.get_next(
                                      data_fp,
                                      data_parser,
                                      scorekeeper)],
                on_disabled_click=on_disabled,
                scale_factor=scale_factor
            ),
            'save': Button(
                corners=[(1586, 692), (1866, 700), (1866, 856), (1582, 840)],
                on_click=lambda: [scorekeeper.save(self.humanoid),
                                  self.update_ui(scorekeeper),
                                  self.get_next(
                                      data_fp,
                                      data_parser,
                                      scorekeeper)],
                on_disabled_click=on_disabled,
                scale_factor=scale_factor
            ),
            'scram': Button(
                corners=[(1578, 852), (1864, 856), (1862, 1036), (1574, 1010)],
                on_click=lambda: [scorekeeper.scram(),
                                  self.update_ui(scorekeeper),
                                  self.get_next(
                                      data_fp,
                                      data_parser,
                                      scorekeeper)],
                on_disabled_click=on_disabled,
                scale_factor=scale_factor
            ),
        }

        # bind button on click callback
        self.root.bind("<Button-1>", lambda e: [button.on_click_callback(e) for button in buttons.values()], add="+")

        # on hover - change cursor to click arrow
        def on_move_callback(e):
            if any([button.is_touching(e.x, e.y) for button in buttons.values()]):
                self.root.config(cursor="hand2")
            else:
                self.root.config(cursor="arrow")
        self.root.bind("<Motion>", on_move_callback, add="+")

        self.button_menu = ButtonMenu(buttons)

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
