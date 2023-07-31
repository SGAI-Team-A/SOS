from gameplay.enums import State, Occupation, Age, Gender
from gameplay.names import generate_name
import random

class Humanoid(object):
    """
    Are they a human or a zombie???
    """

    def __init__(self, fp, state, occupation, age=None, gender=None):
        self.fp = fp
        self.state = state
        self.occupation = occupation
        #
        # if age == Age.YOUNG.value:
        #     lower_bound = 8
        #     upper_bound = 17
        # elif age == Age.MIDDLE.value:
        #     lower_bound = 18
        #     upper_bound = 54
        #     if self.is_doctor():
        #         lower_bound = 25
        #     elif self.is_engineer():
        #         lower_bound = 20
        # elif age == Age.OLD.value:
        #     lower_bound = 55
        #     upper_bound = 80
        #     if self.is_doctor():
        #         upper_bound = 65
        #     elif self.is_engineer():
        #         upper_bound = 70
        # self.age = random.randint(lower_bound, upper_bound)
        #
        # self.gender = gender
        # self.name = generate_name(self.gender)

    def is_zombie(self):
        return self.state == State.ZOMBIE.value

    def is_injured(self):
        return self.state == State.INJURED.value

    def is_infected(self):
        if self.state == State.INJURED.value:
            rand_num = random.random()
            if rand_num < 0.15:
                self.state = State.INFECTED.value
                # print("infected")
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
            scorekeeper.set_update("You took in an engineer and got +1 hour of time!")
        elif self.is_doctor():
            scorekeeper.gain_cure()
            scorekeeper.set_update("You took in a doctor and got +1 cure (save the next injured).")

    def cure(self, scorekeeper):
        # print("cured!")
        self.state = State.HEALTHY.value

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_state(self):
        return self.state

    def get_occupation(self):
        return self.occupation
    
    def get_gender(self):
        return self.gender

    def get_obs_dict(self):
        return {
            "state": self.state,
            "occupation": self.occupation,
            "age": self.age,
            "gender": self.gender,
            "name": self.name
        }