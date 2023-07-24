
class Button(object):
    def __init__(self, x: int, y: int, width: int, height: int, on_click, on_disabled_click):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on_click = on_click
        self.on_disabled_click = on_disabled_click
        self.disabled = False

    def is_touching(self, mouse_x, mouse_y) -> bool:
        return abs(mouse_x - self.x) <= self.width / 2 and abs(mouse_y - self.y) <= self.height

    def callback(self, event) -> None:
        if self.is_touching(event.x, event.y):
            if not self.disabled:
                self.on_click()
            else:
                self.on_disabled_click()

    def set_disabled(self, disabled: bool) -> None:
        self.disabled = disabled