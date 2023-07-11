import math
import tkinter as tk


class CapacityMeter(object):
    def __init__(self, root, w, h, max_cap):
        self.canvas = tk.Canvas(root, width=math.floor(0.2 * w), height=math.floor(0.3 * h))
        self.canvas.place(x=math.floor(0.75 * w), y=math.floor(0.4 * h))
        self.__units = []
        self.unit_size = 40
        self.canvas.update()
        self.render(max_cap, self.unit_size)

    def render(self, max_cap, size):
        tk.Label(self.canvas, text="Capacity", font=("Arial", 15)).place(x=100, y=0)

        x = 3
        y = 50
        for i in range(0, max_cap):
            self.__units.append(create_unit(self.canvas, x, y, size))
            x += size * 1.5
            if (x + size * 1.5) > self.canvas.winfo_width():
                x = 3
                y += size * 1.5

    def update_fill(self, index):
        if index != 0:
            self.canvas.itemconfig(self.__units[index-1], stipple="")
        else:
            for unit in self.__units:
                self.canvas.itemconfig(unit, stipple="gray25")


def create_unit(canvas, x, y, size):
    return canvas.create_rectangle(x, y, x+size, y+size, fill='midnightblue', stipple="gray25")
