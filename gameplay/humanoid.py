from gameplay.enums import State, Occupation
import random


class Humanoid(object):
    """
    Are they a human or a zombie???
    """

    def __init__(self, fp, state, occupation):
        self.fp = fp
        self.state = state
        self.occupation = occupation

    def is_zombie(self):
        return self.state == State.ZOMBIE.value

    def is_injured(self):
        return self.state == State.INJURED.value

    def is_infected(self):
        if self.state == State.INJURED.value:
            randNum = random.randint(0, 9)
            if randNum == 0 or randNum == 1:
                self.state = State.INFECTED.value
                print("infected")
        return self.state == State.INFECTED.value

    def is_healthy(self):
        return self.state == State.HEALTHY.value

    def is_corpse(self):
        return self.state == State.CORPSE.value

    def is_doctor(self):
        return self.occupation == Occupation.DOCTOR.value

    def is_engineer(self):
        return self.occupation == Occupation.ENGINEER.value

    def perform_action(self, scorekeeper):
        if self.is_engineer():
            scorekeeper.gain_battery()
        elif self.is_doctor():
            scorekeeper.gain_cure()

    def cure(self, scorekeeper):
        print("cured!")
        self.state = State.HEALTHY.value
        self.perform_action(scorekeeper)