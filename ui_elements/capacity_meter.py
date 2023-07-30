import math
import tkinter as tk

# green = healthy
# yellow = injured
# red = infected/zombie (deprecated?)

class CapacityMeter(object):
    def __init__(self, root, w, h, max_cap):
        self.canvas = root
        self.__units = []
        self.unit_size = 31
        self.x = w/2
        self.y = h/2
        self.maximum = max_cap

        self.canvas.update()
        self.render(self.unit_size)

    def render(self, size):
        self.canvas.delete('meter')
        pixel_scaling = 1.49
        init_x = self.x - math.floor(size * pixel_scaling * 5/2) + 28
        init_y = 610
        
        x = init_x
        y = init_y
        for i in range(0, self.maximum):
            self.__units.append(create_unit(self.canvas, x, y, size))
            x += size * pixel_scaling
            if (x + size * pixel_scaling) > (init_x + size * pixel_scaling * 5 + 4):
                x = init_x
                y += size * pixel_scaling

    def update_fill(self, index, type):
        color = "gray25" 
        if index != 0: 
            if type == "healthy": #the best code
                color = "green"
            elif type == "injured":
                color = "yellow"
            elif type == "corpse" or "zombie":
                color = "red"
            else:
                color = "gray25"

            self.canvas.itemconfig(self.__units[index-1], fill=color)
        else:
            for unit in self.__units:
                self.canvas.itemconfig(unit, fill=color)
        self.canvas.tag_raise('meter')
    
    def get_size(self):
        return self.unit_size
    
def create_unit(canvas, x, y, size):
    return canvas.create_rectangle(x, y, x+size, y+size, fill='gray25', tags='meter')
