import math
import tkinter as tk
import os
from PIL import ImageTk, Image

from gameplay.enums import Action
from ui_elements.update_log import UpdateLog
from ui_elements.clock import Clock
from ui_elements.status_card import StatusCard
from ui_elements.capacity_meter import CapacityMeter
from ui_elements.cures import CureCounter
from ui_elements.button import Button
from ui_elements.button_menu import ButtonMenu


class HUD(object):
    def __init__(self, ui, root, w, h):
        self.ui = ui
        self.canvas = root
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'post-render.png')
        self.ambulance = ImageTk.PhotoImage(Image.open(self.path).resize((w, h), Image.LANCZOS))
        scale_factor = w / 1920

        self.hud_img = root.create_image(0, 0, anchor=tk.NW, image=self.ambulance, tags='hud')

        self.status_card = StatusCard(self.canvas, 30, 30)
        self.status_card.create(self.ui.humanoid)

        self.cure_counter = CureCounter(root, self.ui.scorekeeper, 30, 200)
        self.cure_counter.build()

        self.clock = Clock(self.canvas, w, h, self.ui.scorekeeper)
        self.meter = CapacityMeter(self.canvas, w, h, self.ui.data_parser.capacity)

        # set up the buttons
        def on_disabled():
            self.update_log.set_update("Action is disabled!"),

        self.buttons = {
            'skip': Button(
                corners=[(1284, 675), (1550, 683), (1540, 832), (1280, 820)],
                on_click=lambda: [
                    self.ui.data_logger.log_action(self.ui.rounds, Action.SKIP.value, self.ui.get_observation()),
                    self.ui.scorekeeper.skip(self.ui.humanoid),
                    self.ui.update_ui(),
                    self.ui.get_next()],
                on_disabled_click=on_disabled,
                scale_factor=scale_factor
            ),
            'squish': Button(
                corners=[(1280, 825), (1542, 840), (1540, 996), (1275, 972), ],
                on_click=lambda: [
                    self.ui.data_logger.log_action(self.ui.rounds, Action.SQUISH.value, self.ui.get_observation()),
                    self.ui.scorekeeper.squish(self.ui.humanoid),
                    self.ui.update_ui(),
                    self.ui.get_next()],
                on_disabled_click=on_disabled,
                scale_factor=scale_factor
            ),
            'save': Button(
                corners=[(1554, 682), (1850, 687), (1846, 852), (1550, 834)],
                on_click=lambda: [
                    self.ui.data_logger.log_action(self.ui.rounds, Action.SAVE.value, self.ui.get_observation()),
                    self.ui.scorekeeper.save(self.ui.humanoid),
                    self.ui.update_ui(),
                    self.ui.get_next()],
                on_disabled_click=on_disabled,
                scale_factor=scale_factor
            ),
            'scram': Button(
                corners=[(1550, 840), (1847, 856), (1845, 1022), (1548, 996)],
                on_click=lambda: [
                    self.ui.data_logger.log_action(self.ui.rounds, Action.SCRAM.value, self.ui.get_observation()),
                    self.ui.scorekeeper.scram(),
                    self.ui.update_ui(),
                    self.ui.get_next()],
                on_disabled_click=on_disabled,
                scale_factor=scale_factor
            ),
        }

        # on hover - change cursor to click arrow
        def on_move_callback(e):
            # buttons aren't showing
            if not any([button.is_on_game_screen() for button in self.buttons.values()]):
                return
            # normal buttons
            elif any([button.is_touching(e.x, e.y) and not button.is_disabled() for button in self.buttons.values()]):
                self.ui.set_cursor("hand2")
            # buttons are disabled
            elif any([button.is_touching(e.x, e.y) and button.is_disabled() for button in self.buttons.values()]):
                self.ui.set_cursor("X_cursor")
            # not touching buttons
            elif not any([button.is_touching(e.x, e.y) for button in self.buttons.values()]):
                self.ui.set_cursor("arrow")

        self.ui.root.bind("<Motion>", on_move_callback, add="+")

        self.button_menu = ButtonMenu(self.buttons)
        self.button_menu.set_interactive(False)

        self.ui.root.bind("<Button-1>", lambda e: self.ui.intro_cards.show_next())

        self.update_log = UpdateLog(self.canvas)

    def build_hud(self, root):
        root.lift(self.hud_img)

    def update(self, humanoid):
        self.build_hud(self.canvas)
        self.update_else()
        self.status_card.create(humanoid)

    def update_else(self):
        self.clock.update_time(self.ui.scorekeeper)
        self.update_log.set_update(self.ui.scorekeeper.get_update())
        self.meter.update_fill(self.ui.scorekeeper.get_current_capacity(), self.ui.scorekeeper.get_last_saved())
        self.cure_counter.update_text()

    # nuke info card on click and make buttons interaction
    def nuke(self, event=None):
        self.ui.root.unbind("<Button-1>")

        # bind button on click callback
        self.ui.root.bind("<Button-1>", lambda e: [button.on_click_callback(e) for button in self.buttons.values()],
                          add="+")
        self.button_menu.set_interactive(True)

        if self.ui.real_time_enabled:
            self.clock.count_down_real_time(self.ui, self.ui.scorekeeper)

