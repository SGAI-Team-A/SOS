import random
from gameplay.enums import State
class injured(Humanoid):
    def is_infected(self):
        if self.state == State.INJURED.value:
            randNum = random.randint(0,9)
            if randNum == 0 or randNum == 1:
                self.state = State.INFECTED
        return self.state == State.InFECTED.value

        