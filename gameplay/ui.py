import tkinter as tk

from ui_elements.button import Button
from ui_elements.button_menu import ButtonMenu
from ui_elements.game_viewer import GameViewer
from os.path import join


class UI(object):
    def __init__(self, data_parser, scorekeeper, data_fp, is_disable):
        #  Base window setup
        w, h = 1280, 720
        scale_factor = w / 1920  # original image size is 1920 by 1080
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
        self.game_viewer = GameViewer(self.frame, w, h, data_fp, self.humanoid, scorekeeper, data_parser)
        self.root.bind("<Delete>", self.game_viewer.delete_photo)

        # set up the buttons
        def on_disabled():
            self.game_viewer.hud.update_log.set_update("Not enough time left!"),

        buttons = {
            'skip': Button(
                corners=[(1284, 675), (1550, 683), (1540, 832), (1280, 820) ],
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
                corners=[(1280, 825), (1542, 840), (1540, 996), (1275, 972),],
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
                corners=[(1554, 682), (1850, 687), (1846, 852), (1550, 834)],
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
                corners=[(1550, 840), (1847, 856), (1845, 1022), (1548, 996)],
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
            # buttons aren't showing
            if any([button.is_touching(e.x, e.y) and not button.is_on_game_screen() for button in buttons.values()]):
                self.root.config(cursor="arrow")
            # normal buttons
            elif any([button.is_touching(e.x, e.y) and not button.is_disabled() for button in buttons.values()]):
                self.root.config(cursor="hand2")
            # buttons are disabled
            elif any([button.is_touching(e.x, e.y) and button.is_disabled() for button in buttons.values()]):
                self.root.config(cursor="X_cursor")
            # not touching buttons
            else:
                self.root.config(cursor="arrow")
        self.root.bind("<Motion>", on_move_callback, add="+")

        self.button_menu = ButtonMenu(buttons)
        self.button_menu.set_interactive(False)

        # nuke info card on click and make buttons interaction
        self.game_viewer.canvas.tag_bind("info_card", "<ButtonRelease-1>", lambda e: [
            self.game_viewer.info_card.nuke(e),
            self.button_menu.set_interactive(True),

        ])

        self.root.mainloop()

    def update_ui(self, scorekeeper):
        self.game_viewer.update_else()

    def on_resize(self, event):
        w, h = 0.6 * self.root.winfo_width(), 0.7 * self.root.winfo_height()
        self.game_viewer.canvas.config(width=w, height=h)

    def get_next(self, data_fp, data_parser, scorekeeper):
        remaining = len(data_parser.unvisited)

        # Ran out of humanoids? Disable skip/save/squish
        if remaining == 0 or scorekeeper.remaining_time <= 0:
            self.game_viewer.hud.meter.update_fill(0, None)
           # self.game_viewer.delete_photo(None)
            self.game_viewer.display_score(scorekeeper.get_score(), self.frame)
            self.button_menu.disable_buttons(scorekeeper.remaining_time, remaining, scorekeeper.at_capacity())
            self.game_viewer.hud.update_log.set_update("")
        else:
            humanoid = data_parser.get_random()
            # Update visual display
            self.humanoid = humanoid
            fp = join(data_fp, self.humanoid.fp)
            self.game_viewer.update(fp, self.humanoid)

        # Disable button(s) if options are no longer possible
        self.button_menu.disable_buttons(scorekeeper.remaining_time, remaining, scorekeeper.at_capacity())
