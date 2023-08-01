import math
import tkinter as tk
from os.path import join
from PIL import ImageTk, Image, ImageGrab, ImageFilter
from ui_elements.hud import HUD
from ui_elements.score_screen import ScoreScreen


class GameViewer(object):
    """"
    Graphics curtesy of Lucas
    """
    def __init__(self, ui, root, w, h):
        self.ui = ui
        self.width = w
        self.height = h
        self.root = root

        self.scale_factor = 1
        self.canvas = tk.Canvas(root, width=self.width, height=self.height)
        self.canvas.place(x=0,y=0)
        self.canvas.update()

        self.photo = None
        self.create_photo(join(self.ui.data_fp, self.ui.humanoid.fp))

        self.hud = HUD(self.ui, self.canvas, self.width, self.height)
        self.hud.build_hud(self.canvas)

        self.update_else()

    def restart_game(self):
        # reset game controllers
        self.ui.reset_game()

        # clear canvas
        self.canvas.delete("all")
        self.score_screen.bg.destroy()

        # recreate hud
        self.create_photo(join(self.ui.data_fp, self.ui.humanoid.fp))
        self.hud = HUD(self.ui, self.canvas, self.width, self.height)
        self.hud.build_hud(self.canvas)

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
        self.photo = display_photo(fp, math.floor(self.canvas.winfo_width() * self.scale_factor),
                                   math.floor(self.canvas.winfo_height() * self.scale_factor))
        self.canvas.create_image(
            (self.canvas.winfo_width() * 0.5) - math.floor(self.scale_factor * self.canvas.winfo_width() * 0.5), 0,
            anchor=tk.NW, image=self.photo, tags='photo')

    def display_score(self, score, window):
        self.ui.set_cursor()

        self.hud.status_card.remove()
        self.hud.cure_counter.remove()

        x = window.winfo_rootx()
        y = window.winfo_rooty()
        width = window.winfo_width()
        height = window.winfo_height()
        self.canvas.delete("all")
        image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        blur = image.filter(ImageFilter.GaussianBlur(radius=10))
        self.im_final = ImageTk.PhotoImage(blur.resize((width, height), Image.LANCZOS))
        self.canvas.create_image(0, 0, image=self.im_final, anchor=tk.NW)

        self.score_screen = ScoreScreen(self.canvas, score, self)

def display_photo(img_path, w, h):
    img = Image.open(img_path)
    resized = img.resize((w, h), Image.LANCZOS)

    tk_img = ImageTk.PhotoImage(resized)
    return tk_img
