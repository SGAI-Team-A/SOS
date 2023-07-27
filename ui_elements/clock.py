import tkinter as tk
import math
import os
import PIL
from ui_elements.render_font import RenderFont

# class
class Clock(object):
    def __init__(self, root, w, h, scorekeeper):
        self.canvas = root
        self.x = w/2  # Center Point x
        self.y = w/2  # Center Point

        font_path = (os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'Digital-7.ttf'))
        self.clock_font = RenderFont(filename=font_path, fill="green")

        self.update_time(scorekeeper)

    def update_time(self, scorekeeper):
        h = (math.floor(scorekeeper.remaining_time / 60.0))
        m = max(scorekeeper.remaining_time % 60, 0)
        if h < 0:
            h = 0
            m = 0
        time = '{:02d}:{:02d}'.format(h, m)
        self.time_render = PIL.ImageTk.PhotoImage(self.clock_font.get_render(font_size=70, txt=time))
        self.canvas.delete("clock")
        self.canvas.create_image(self.x + 35, 60, image=self.time_render, tags="clock")

        return

    def get_time_render(self):
        return self.time_render
    

# # Main Function Trigger
# if __name__ == '__main__':
#     root = Clock()
#
#     # Creating Main Loop
#     while True:
#         root.update()
#         root.update_idletasks()
#         root.update_class(12, 15)
