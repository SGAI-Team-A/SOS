import tkinter as tk
from endpoints.data_logger import DataLogger
from endpoints.data_parser import DataParser
from gameplay.scorekeeper import ScoreKeeper
from ui_elements.game_viewer import GameViewer
from os.path import join
from ui_elements.intro_cards import IntroCards


class UI(object):
    def __init__(self, data_parser: DataParser, scorekeeper: ScoreKeeper, data_fp, data_logger: DataLogger, is_disable, rounds = 0):
        self.data_parser = data_parser
        self.scorekeeper = scorekeeper
        self.data_fp = data_fp
        self.data_logger = data_logger
        self.humanoid = data_parser.get_random()

        # number of rounds played
        self.rounds = rounds

        #  Base window setup
        w, h = 1280, 720  # original image size is 1920 by 1080
        self.root = tk.Tk()
        self.root.title("Beaverworks SGAI 2023 - Dead or Alive")
        self.root.geometry(str(w) + 'x' + str(h))
        self.root.resizable(False, False)

        self.frame = tk.Frame(self.root, width=w, height=h)
        self.frame.place(x=0, y=0)

        if not is_disable:
            # self.machine_interface = MachineInterface(self.frame, w, h)
            pass

        #  Display the game
        self.game_viewer = GameViewer(self, self.frame, w, h)
        self.root.bind("<Delete>", self.game_viewer.delete_photo)
        self.game_ended = False
        self.real_time_enabled = False

        self.intro_cards = IntroCards(self.frame, w, h, self.game_viewer.hud.nuke, self)

        self.root.mainloop()

    def reset_game(self):
        self.data_parser.reset_game()
        self.scorekeeper = ScoreKeeper(self.data_parser.shift_length, self.data_parser.capacity)
        self.humanoid = self.data_parser.get_random()
        self.game_ended = False

        self.rounds += 1

        # reset buttons
        self.game_viewer.hud.button_menu.set_interactive(True)
        self.game_viewer.hud.button_menu.disable_buttons(self.scorekeeper.remaining_time, len(self.data_parser.unvisited), self.scorekeeper.at_capacity())
        if self.real_time_enabled:
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
        # get next humanoid
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

    def get_observation(self):
        obs = self.humanoid.get_obs_dict()
        obs['capacity'] = self.data_parser.capacity
        obs['time'] = self.scorekeeper.remaining_time
        obs['cures'] = self.scorekeeper.get_cures()

        return obs
    
    def set_real_time(self, time):
        self.real_time_enabled = time

    def end_game(self, remaining):
      if not self.game_ended:
          # log results
          self.data_logger.log_results(self.rounds, self.scorekeeper.get_score())

          # update ui
          self.game_viewer.hud.meter.update_fill(0, None)
          self.game_viewer.display_score(self.scorekeeper.get_score(), self.frame)
          self.game_viewer.hud.button_menu.disable_buttons(self.scorekeeper.remaining_time, remaining, self.scorekeeper.at_capacity())
          self.game_viewer.hud.update_log.set_update("")
          self.game_ended = True
        
