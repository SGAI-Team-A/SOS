import math
import tkinter as tk
import os
from os.path import join
from PIL import ImageTk, Image, ImageGrab, ImageFilter
from ui_elements.hud import HUD
from ui_elements.update_log import UpdateLog
from ui_elements.clock import Clock
from ui_elements.status_card import StatusCard
from ui_elements.capacity_meter import CapacityMeter
from ui_elements.score_screen import ScoreScreen

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

        self.hud = HUD(self.canvas, w, h, humanoid, data_parser, self.scorekeeper)
        self.hud.build_hud(self.canvas)

        self.info_card = InfoCard(self.canvas, w, h)
        self.info_card.lift_(self.canvas)
        self.canvas.tag_bind("info_card", "<Button-1>", self.info_card.nuke)
        
        self.update_else()

    def update(self, fp, humanoid):
        self.create_photo(fp)
        self.hud.update(humanoid)
    
    def update_else(self):
        self.hud.update_else()

    def delete_photo(self, event=None):
        self.canvas.delete('photo')

    def create_photo(self, fp):
        self.canvas.delete('photo')
        self.photo = display_photo(fp, math.floor(self.canvas.winfo_width() * self.scale_factor), math.floor(self.canvas.winfo_height() * self.scale_factor))
        self.canvas.create_image((self.canvas.winfo_width() * 0.5) - math.floor(self.scale_factor * self.canvas.winfo_width() * 0.5), 0, anchor=tk.NW, image=self.photo, tags='photo')

    def display_score(self, score, window):
        self.hud.status_card.remove()
        x = window.winfo_rootx()
        y = window.winfo_rooty()
        width = window.winfo_width()
        height = window.winfo_height()
        self.canvas.delete("all")
        image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        blur = image.filter(ImageFilter.GaussianBlur(radius=10))
        self.im_final = ImageTk.PhotoImage(blur.resize((width, height), Image.LANCZOS))
        self.canvas.create_image(0, 0, image=self.im_final, anchor=tk.NW)
        self.score_screen = ScoreScreen(self.canvas, score)

def display_photo(img_path, w, h):
    img = Image.open(img_path)
    resized = img.resize((w, h), Image.LANCZOS)

    tk_img = ImageTk.PhotoImage(resized)
    return tk_img

class InfoCard(object):
    def __init__(self, root, w, h):
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'info-card.png')
        self.info_card = display_photo(self.path, w, h)
        self.root = root
        self.build(self.root)
    
    def build(self, root):
        self.image = root.create_image(0, 0, anchor=tk.NW, image=self.info_card, tags='info_card')

    def nuke(self, event=None):
        try:
            self.root.delete("info_card")
            self.root.unbind('info_card',"<Button-1>")
        except tk.TclError as e:
            pass
    
    def lift_(self, root):
        root.lift(self.image)