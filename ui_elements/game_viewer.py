import math
import tkinter as tk
from os.path import join
from PIL import ImageTk, Image
from ui_elements.hud import HUD
from ui_elements.update_log import UpdateLog
from ui_elements.clock import Clock
from ui_elements.status_card import StatusCard
from ui_elements.capacity_meter import CapacityMeter

class GameViewer(object):
    def __init__(self, root, w, h, data_fp, humanoid, scorekeeper, data_parser):
        self.scale_factor = 0.9
        self.canvas = tk.Canvas(root, width=w, height=h)
        self.canvas.place(x=0, y=0)
        self.canvas.update()
        self.width = w
        self.height = h
        self.scorekeeper = scorekeeper

        self.photo = None
        self.create_photo(join(data_fp, humanoid.fp))

        self.status_card = StatusCard(self.canvas, 40,30)
        self.status_card.create(humanoid)

        self.hud = HUD(self.canvas, w, h)
        self.hud.build_hud(self.canvas)

        self.clock = Clock(self.canvas, w, h, self.scorekeeper)
        self.meter = CapacityMeter(self.canvas, w, h, data_parser.capacity)

        self.update_log = UpdateLog(self.canvas)
        self.update_else()

    def update(self, fp, humanoid):
        self.create_photo(fp)
        self.hud.build_hud(self.canvas)
        self.update_else()
        self.status_card.create(humanoid)
    
    def update_else(self):
        self.clock.update_time(self.scorekeeper)
        self.update_log.set_update(self.scorekeeper.get_update())
        self.meter.update_fill(self.scorekeeper.get_current_capacity(), self.scorekeeper.get_last_saved())

    def delete_photo(self, event=None):
        self.canvas.delete('photo')

    def create_photo(self, fp):
        self.canvas.delete('photo')
        self.photo = display_photo(fp, math.floor(self.canvas.winfo_width() * self.scale_factor), math.floor(self.canvas.winfo_height() * self.scale_factor))
        self.canvas.create_image((self.canvas.winfo_width() * 0.5) - math.floor(self.scale_factor * self.canvas.winfo_width() * 0.5), 0, anchor=tk.NW, image=self.photo, tags='photo')

    def display_score(self, score):
        self.status_card.destroy()
        tk.Label(self.canvas, text="FINAL SCORE", font=("Arial", 30)).pack(anchor=tk.N)
        tk.Label(self.canvas, text="Killed {}".format(score["killed_z"]) + " zombies", font=("Arial", 15)).pack(anchor=tk.N)
        tk.Label(self.canvas, text="Killed {}".format(score["killed_h"]) + " humans", font=("Arial", 15)).pack(anchor=tk.N)
        tk.Label(self.canvas, text="Saved {}".format(score["saved_z"]) + " zombies", font=("Arial", 15)).pack(anchor=tk.N)
        tk.Label(self.canvas, text="Saved {}".format(score["saved_h"]) + " humans", font=("Arial", 15)).pack(anchor=tk.N)


def display_photo(img_path, w, h):
    img = Image.open(img_path)
    resized = img.resize((w, h), Image.LANCZOS)

    tk_img = ImageTk.PhotoImage(resized)
    return tk_img
