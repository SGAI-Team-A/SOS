from gameplay.enums import State, Occupation
from gameplay.names import generate_name
import random

class Humanoid(object):
    """
    Are they a human or a zombie???
    """

    def __init__(self, fp, state, occupation, age=None, name=None):
        self.fp = fp
        self.state = state
        self.occupation = occupation

        if age is None:
            self.age = random.randint(8, 80)
        else:
            self.age = age

        if name is None:
            self.name = generate_name()
        else:
            self.name = name

    def is_zombie(self):
        return self.state == State.ZOMBIE.value

    def is_injured(self):
        return self.state == State.INJURED.value

    def is_infected(self):
        if self.state == State.INJURED.value:
            rand_num = random.randint(0, 9)
            if rand_num == 0 or rand_num == 1:
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

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_state(self):
        return self.state

    def get_occupation(self):
        return self.state
