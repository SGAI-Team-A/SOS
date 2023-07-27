import tkinter as tk

class StatusCard(object):
    def __init__(self, root, x, y):
        self.stat_card = tk.Canvas(
            root,
            background='white',
            borderwidth=1,
            relief="flat",
        )
        self.x = x
        self.y = y
        self.labels = []
    
    def create(self, humanoid):
        self.stat_card.place(x=self.x, y=self.y)
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

    def remove(self):
        self.stat_card.destroy()
        
