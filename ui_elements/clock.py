import tkinter as tk
import os
import math


# class
class Clock(object):
    def __init__(self, root, w, h, init_h, init_m):
        self.canvas = tk.Canvas(root, width=math.floor(0.2 * w), height=math.floor(0.3 * h))
        self.canvas.place(x=math.floor(0.75 * w), y=50)
        self.sticks = None
        self.image = None
        self.x = 150  # Center Point x
        self.y = 150  # Center Point
        self.length = [30, 55]  # Stick Length
        self.width = [3, 6]
        self.fill = ['red', 'midnight blue']

        self.render()
        self.update_time(init_h, init_m)

    def render(self):
        tk.Label(self.canvas, text="Remaining time", font=("Arial", 15)).place(x=80, y=30)
        self.generate_bg()
        self.generate_clock_hands()
        return

    def generate_bg(self):
        self.image = tk.PhotoImage(file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics', 'clock.gif'))  #'/home/ly30959/catkin_ws/SGAI_2023/data/clock.gif')
        self.canvas.create_image(self.x, self.y, image=self.image)
        return

    def generate_clock_hands(self):
        self.sticks = []
        for i in range(2):
            store = self.canvas.create_line(self.x, self.y, self.x + self.length[i], self.y + self.length[i],
                                            width=self.width[i-1], fill=self.fill[i])
            self.sticks.append(store)
        return

    def update_time(self, h, m):
        now = (h * 5, m)
        # Changing Stick Coordinates
        for n, i in enumerate(now):
            x, y = self.canvas.coords(self.sticks[n])[0:2]
            cr = [x, y, self.length[n] * math.cos(math.radians(i * 6) - math.radians(90)) + self.x,
                  self.length[n] * math.sin(math.radians(i * 6) - math.radians(90)) + self.y]
            self.canvas.coords(self.sticks[n], tuple(cr))
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
