import math
import tkinter as tk
from os.path import join
from PIL import ImageTk, Image
from ui_elements.hud import HUD


class GameViewer(object):
    def __init__(self, root, w, h, data_fp, humanoid):
        self.scale_factor = 0.9
        self.canvas = tk.Canvas(root, width=w, height=h)
        self.canvas.place(x=0, y=0)
        self.canvas.update()
        self.width = w
        self.height = h

        self.photo = None
        self.create_photo(join(data_fp, humanoid.fp))

        self.stat_card = tk.Canvas(
            root,
            background='white',
            borderwidth=1,
            relief="flat",
        )
        self.stat_card.place(x=350, y=150)
        self.labels = []
        self.create_stat_card(humanoid)

        self.hud = HUD(self.canvas, w, h)
        self.hud.build_hud(self.canvas)

    def update(self, fp, humanoid):
        self.create_photo(fp)
        self.hud.build_hud(self.canvas)
        self.create_stat_card(humanoid)

    def delete_photo(self, event=None):
        self.canvas.delete('photo')

    def create_photo(self, fp):
        self.canvas.delete('photo')
        self.photo = display_photo(fp, math.floor(self.canvas.winfo_width() * self.scale_factor), math.floor(self.canvas.winfo_height() * self.scale_factor))
        self.canvas.create_image((self.canvas.winfo_width() * 0.5) - math.floor(self.scale_factor * self.canvas.winfo_width() * 0.5), 0, anchor=tk.NW, image=self.photo, tags='photo')

    def create_stat_card(self, humanoid):
        for label in self.labels:
            label.destroy()

        self.labels = [
            tk.Label(self.stat_card, text="{}".format(humanoid.get_name()), font=("Arial", 20)),
            tk.Label(self.stat_card, text="~~ {} ~~".format(humanoid.get_state().capitalize()), font=("Arial", 15)),
            tk.Label(self.stat_card, text="Age: {}".format(humanoid.get_age()), font=("Arial", 15)),
            tk.Label(self.stat_card, text="Occupation: {}".format(humanoid.get_occupation().capitalize()), font=("Arial", 15))
        ]
        for label in self.labels:
            label.pack(anchor=tk.N, padx=10)
            label.config(bg="white")
        self.labels[0].pack(pady=(10,0))
        self.labels[len(self.labels) - 1].pack(pady=(0,10))
        self.stat_card.update()

    def destroy_stat_card(self):
        self.stat_card.destroy()

    def display_score(self, score):
        self.destroy_stat_card()
        tk.Label(self.canvas, text="FINAL SCORE", font=("Arial", 30)).pack(anchor=tk.NW)
        tk.Label(self.canvas, text="Killed {}".format(score["killed_z"]) + " zombies", font=("Arial", 15)).pack(anchor=tk.NW)
        tk.Label(self.canvas, text="Killed {}".format(score["killed_h"]) + " humans", font=("Arial", 15)).pack(anchor=tk.NW)
        tk.Label(self.canvas, text="Saved {}".format(score["saved_z"]) + " zombies", font=("Arial", 15)).pack(anchor=tk.NW)
        tk.Label(self.canvas, text="Saved {}".format(score["saved_h"]) + " humans", font=("Arial", 15)).pack(anchor=tk.NW)


def display_photo(img_path, w, h):
    img = Image.open(img_path)
    resized = img.resize((w, h), Image.LANCZOS)

    tk_img = ImageTk.PhotoImage(resized)
    return tk_img
