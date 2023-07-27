import math
import tkinter as tk
import os
from os.path import join
from PIL import ImageTk, Image
from ui_elements.update_log import UpdateLog
from ui_elements.clock import Clock
from ui_elements.status_card import StatusCard
from ui_elements.capacity_meter import CapacityMeter
from ui_elements.cures import CureCounter

class HUD(object):
    def __init__(self, ui, root, w, h):
        self.ui = ui
        self.canvas = root
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'post-render.png')
        self.ambulance = ImageTk.PhotoImage(Image.open(self.path).resize((w, h), Image.LANCZOS))

        self.hud_img = root.create_image(0, 0, anchor=tk.NW, image=self.ambulance, tags='hud')

        self.status_card = StatusCard(self.canvas, 30,30)
        self.status_card.create(self.ui.humanoid)

        self.cure_counter = CureCounter(root, self.ui.scorekeeper, 30, 200)
        self.cure_counter.build()

        self.clock = Clock(self.canvas, w, h, self.ui.scorekeeper)
        self.meter = CapacityMeter(self.canvas, w, h, self.ui.data_parser.capacity)

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


