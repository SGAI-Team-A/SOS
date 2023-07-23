import tkinter as tk
import math

# class
class Clock(object):
    def __init__(self, root, w, h, init_h, init_m):
        self.canvas = tk.Canvas(root, width=math.floor(0.2 * w), height=math.floor(0.3 * h))
        self.canvas.place(x=math.floor(0.75 * w), y=50)
        self.image = None
        self.x = 150  # Center Point x
        self.y = 150  # Center Point
        self.time_label = self.set_time('')

        self.render()
        self.update_time(init_h, init_m)
        

    def render(self):
        tk.Label(self.canvas, text="Remaining time", font=("Arial", 15)).place(x=80, y=30)
        return

    def update_time(self, h, m):
        time = '{:02d}:{:02d}'.format(h, m)
        self.time_label = self.set_time(time)
        
        return
    
    def set_time(self, time):
        return tk.Label(self.canvas, text=time, font=("Arial", 15)).place(x=80, y=140)


# # Main Function Trigger
# if __name__ == '__main__':
#     root = Clock()
#
#     # Creating Main Loop
#     while True:
#         root.update()
#         root.update_idletasks()
#         root.update_class(12, 15)
