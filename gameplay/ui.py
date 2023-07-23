import math
import tkinter as tk
from ui_elements.button_menu import ButtonMenu
from ui_elements.capacity_meter import CapacityMeter
from ui_elements.clock import Clock
from endpoints.machine_interface import MachineInterface
from ui_elements.game_viewer import GameViewer
from ui_elements.machine_menu import MachineMenu
from os.path import join
from ui_elements.update_log import UpdateLog
from ui_elements.hud import HUD

class UI(object):
    def __init__(self, data_parser, scorekeeper, data_fp, is_disable):
        #  Base window setup
        w, h = 1280, 800
        self.root = tk.Tk()
        self.root.title("Beaverworks SGAI 2023 - Dead or Alive")
        self.root.geometry(str(w) + 'x' + str(h))
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root, width=w, height=h)
        self.frame.place(x=0,y=0)

        self.update_log = UpdateLog(self.frame)
        
        self.humanoid = data_parser.get_random()
        if not is_disable:
            self.machine_interface = MachineInterface(self.frame, w, h)

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

        if not is_disable:
            machine_buttons = [("Suggest", lambda: [self.machine_interface.suggest(self.humanoid)]),
                               ("Act", lambda: [self.machine_interface.act(scorekeeper, self.humanoid),
                                                self.update_ui(scorekeeper),
                                                self.get_next(
                                                    data_fp,
                                                    data_parser,
                                                    scorekeeper)])]
            self.machine_menu = MachineMenu(self.frame, machine_buttons)

        #  Display central photo
        self.game_viewer = GameViewer(self.frame, w, h, data_fp, self.humanoid)
        self.root.bind("<Delete>", self.game_viewer.delete_photo)

        # Display the countdown
        init_h = max((math.floor(scorekeeper.remaining_time / 60.0)), 0)
        init_m = max(scorekeeper.remaining_time % 60, 0)
        self.clock = Clock(self.frame, w, h, init_h, init_m)

        # Display ambulance capacity
        self.capacity_meter = CapacityMeter(self.frame, w, h, data_parser.capacity)

        # displays ambulance hud
        # self.hud = HUD(self.frame, w, h)

        self.root.mainloop()

    def update_ui(self, scorekeeper):
        self.update_clock(scorekeeper)
        self.capacity_meter.update_fill(scorekeeper.get_current_capacity(), scorekeeper.get_last_saved())
         # Creates texts onto the canvas
        self.update_log.set_update(scorekeeper.get_update())
        
    def update_clock(self, scorekeeper):
        h = (math.floor(scorekeeper.remaining_time / 60.0))
        m = max(scorekeeper.remaining_time % 60, 0)
        if h < 0:
            h = 0
            m = 0
        self.clock.update_time(h, m)

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
            self.machine_menu.disable_all_buttons()
            self.button_menu.disable_buttons(scorekeeper.remaining_time, remaining, scorekeeper.at_capacity())
        else:
            humanoid = data_parser.get_random()
            # Update visual display
            self.humanoid = humanoid
            fp = join(data_fp, self.humanoid.fp)
            self.game_viewer.update(fp, self.humanoid)

        # Disable button(s) if options are no longer possible
        self.button_menu.disable_buttons(scorekeeper.remaining_time, remaining, scorekeeper.at_capacity())
