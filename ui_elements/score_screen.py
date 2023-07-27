import tkinter as tk


class ScoreScreen(object):
    def __init__(self, root, score, game_viewer):
        self.bg = tk.Canvas(root, width=400, height=300, bg="white", borderwidth=1)
        self.bg.place(relx=0.5, rely=0.5, anchor="center")

        self.bg.create_text(200, 50, text="RESULTS", font=("Arial", 30), anchor="center")
        self.bg.create_text(200, 100, text="Killed {} zombies".format(score["killed_z"]), font=("Arial", 15),
                            anchor="center")
        self.bg.create_text(200, 130, text="Killed {} humans".format(score["killed_h"]), font=("Arial", 15),
                            anchor="center")
        self.bg.create_text(200, 160, text="Saved {} zombies".format(score["saved_z"]), font=("Arial", 15),
                            anchor="center")
        self.bg.create_text(200, 190, text="Saved {} humans".format(score["saved_h"]), font=("Arial", 15),
                            anchor="center")

        playbutton = self.bg.create_rectangle(150, 220, 250, 250, fill="white", tags="playbutton")
        playtext = self.bg.create_text(200, 235, text="Play Again", tags="playbutton")

        self.bg.tag_bind("playbutton", "<Button-1>", lambda e: game_viewer.restart_game())
        self.bg.tag_bind("playbutton", "<Enter>", lambda e: game_viewer.ui.set_cursor("hand2"))
        self.bg.tag_bind("playbutton", "<Leave>", lambda e: game_viewer.ui.set_cursor())
