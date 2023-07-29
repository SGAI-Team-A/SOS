import tkinter as tk
import asyncio

from gameplay.scorekeeper import ScoreKeeper
from ui_elements.game_viewer import GameViewer
from os.path import join
from ui_elements.intro_cards import IntroCards


class UI(object):
    def __init__(self, data_parser, scorekeeper, data_fp, is_disable):
        self.data_parser = data_parser
        self.scorekeeper = scorekeeper
        self.data_fp = data_fp

        #  Base window setup
        w, h = 1280, 720  # original image size is 1920 by 1080
        self.root = tk.Tk()
        self.root.title("Beaverworks SGAI 2023 - Dead or Alive")
        self.root.geometry(str(w) + 'x' + str(h))
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root, width=w, height=h)
        self.frame.place(x=0, y=0)

        self.humanoid = data_parser.get_random()
        if not is_disable:
            # self.machine_interface = MachineInterface(self.frame, w, h)
            pass

        #  Display the game
        self.game_viewer = GameViewer(self, self.frame, w, h)
        self.root.bind("<Delete>", self.game_viewer.delete_photo)
        self.game_ended = False

        self.intro_cards = IntroCards(self.frame, w, h, self.game_viewer.hud.nuke)

        self.root.mainloop()

    def reset_game(self):
        self.data_parser.reset_game()
        self.scorekeeper = ScoreKeeper(self.data_parser.shift_length, self.data_parser.capacity)
        self.humanoid = self.data_parser.get_random()
        self.game_ended = False

        # reset buttons
        self.game_viewer.hud.button_menu.set_interactive(True)
        self.game_viewer.hud.button_menu.disable_buttons(self.scorekeeper.remaining_time, len(self.data_parser.unvisited), self.scorekeeper.at_capacity())
        self.game_viewer.hud.clock.count_down_real_time(self, self.scorekeeper)

    def update_ui(self):
        self.game_viewer.update_else()

    def on_resize(self, event):
        w, h = 0.6 * self.root.winfo_width(), 0.7 * self.root.winfo_height()
        self.game_viewer.canvas.config(width=w, height=h)

    def get_next(self):
        self.remaining = len(self.data_parser.unvisited)

        # Ran out of humanoids? Disable skip/save/squish
        if self.remaining == 0 or self.scorekeeper.remaining_time <= 0:
            self.end_game(self.remaining)
        else:
            humanoid = self.data_parser.get_random()
            # Update visual display
            self.humanoid = humanoid
            fp = join(self.data_fp, self.humanoid.fp)
            self.game_viewer.update(fp, self.humanoid)

        # Disable button(s) if options are no longer possible
        self.game_viewer.hud.button_menu.disable_buttons(self.scorekeeper.remaining_time, self.remaining, self.scorekeeper.at_capacity())

    def set_cursor(self, cursor_type: str = "arrow"):
        self.root.config(cursor=cursor_type)

    def end_game(self, remaining):
        if not self.game_ended:
            self.game_viewer.hud.meter.update_fill(0, None)
            # self.game_viewer.delete_photo(None)
            self.game_viewer.display_score(self.scorekeeper.get_score(), self.frame)
            self.game_viewer.hud.button_menu.disable_buttons(self.scorekeeper.remaining_time, remaining, self.scorekeeper.at_capacity())
            self.game_viewer.hud.update_log.set_update("")
            self.game_ended = True
        