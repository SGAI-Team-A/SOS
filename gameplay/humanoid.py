from gameplay.enums import State
import random

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
    
    def is_infected(self):
        if self.state == State.INJURED.value:
            randNum = random.randint(0,9)
            if randNum == 0 or randNum == 1:
                self.state = State.INFECTED
                print ("infected")
        return self.state == State.INFECTED.value
    
    def is_healthy(self):
        return self.state == State.HEALTHY.value
    
    def is_corpse(self):
        return self.state == State.CORPSE.value
