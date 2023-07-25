from math import isclose


class Button(object):
    def __init__(self, corners, on_click, on_disabled_click, scale_factor=1):
        # list of tuples: [Top Left, Top Right, Bottom Right, Bottom Left]
        self.corners = [(x*scale_factor, y*scale_factor) for x, y in corners]
        self.on_click = on_click
        self.on_disabled_click = on_disabled_click
        self.disabled = False
        self.on_game_screen = True

        self.area = get_area_triangle(self.corners[:-1]) + get_area_triangle([self.corners[0], self.corners[2], self.corners[3]])

    def is_touching(self, mouse_x, mouse_y) -> bool:
        area = 0
        for i, val in enumerate(self.corners):
            points = self.corners[i: i+2]

            # last side wraparound
            if i == len(self.corners) - 1:
                points = [self.corners[0], self.corners[-1]]

            points.append((mouse_x, mouse_y))
            area += get_area_triangle(points)

        return isclose(area, self.area, abs_tol=1e-8)

    def on_click_callback(self, event) -> None:
        if self.is_touching(event.x, event.y) and self.on_game_screen:
            if not self.disabled:
                self.on_click()
            else:
                self.on_disabled_click()

    def set_disabled(self, disabled: bool) -> None:
        self.disabled = disabled

    def set_on_game_screen(self, on_game_screen=False):
        self.on_game_screen = on_game_screen

    def is_disabled(self):
        return self.disabled

    def is_on_game_screen(self):
        return self.on_game_screen


def get_area_triangle(corners):
    return 0.5 * abs(
        corners[0][0] * (corners[1][1] - corners[2][1]) +
        corners[1][0] * (corners[2][1] - corners[0][1]) +
        corners[2][0] * (corners[0][1] - corners[1][1])
    )