from gameplay.enums import State


class Humanoid(object):
    """
    Are they a human or a zombie???
    """
    def __init__(self, fp, state, value):
        self.fp = fp
        self.state = state
        self.value = value

    def is_zombie(self):
        return self.state == State.ZOMBIE.value

    def is_injured(self):
        return self.state == State.INJURED.value

    def is_healthy(self):
        return self.state == State.HEALTHY.value
