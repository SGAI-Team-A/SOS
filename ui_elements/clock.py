import tkinter as tk
import os
import math
from time import strftime

# class
class Clock(object):
    def __init__(self, root, w, h, init_h, init_m):
        self.canvas = tk.Canvas(root, width=math.floor(0.2 * w), height=math.floor(0.3 * h))
        self.canvas.place(x=math.floor(0.75 * w), y=50)
        self.image = None
        self.x = 150  # Center Point x
        self.y = 150  # Center Point

        self.render()
        self.update_time(init_h, init_m)
        

    def render(self):
        tk.Label(self.canvas, text="Remaining time", font=("Arial", 15)).place(x=80, y=30)
        self.generate_bg()
        return

    def generate_bg(self):
        self.image = tk.PhotoImage(file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'clock.gif'))  #'/home/ly30959/catkin_ws/SGAI_2023/data/clock.gif')
        self.canvas.create_image(self.x, self.y, image=self.image)
        return

    def update_time(self, h, m):
        tk.Label(self.canvas, text=str(h) + " " + str(m), font=("Arial", 15)).place(x=80, y=140)
        
        return


# # Main Function Trigger
# if __name__ == '__main__':
#     root = Clock()
#
#     # Creating Main Loop
#     while True:
#         root.update()
#         root.update_idletasks()
#         root.update_class(12, 15)
