from gameplay.enums import ActionCost


class ScoreKeeper(object):
    def __init__(self, shift_len, capacity):
        self.__ambulance = {
            "zombie": 0,
            "injured": 0,
            "healthy": 0
        }
        self.__scorekeeper = {
            "killed_h": 0,
            "saved_h": 0,
            "killed_z" : 0,
            "saved_z" : 0
        }
        self.__capacity = capacity
        self.remaining_time = int(shift_len)  # minutes

    def save(self, humanoid):
        self.remaining_time -= ActionCost.SAVE.value
        if humanoid.is_zombie():
            self.__ambulance["zombie"] += 1
        elif humanoid.is_injured():
            self.__ambulance["injured"] += 1
        else:
            self.__ambulance["healthy"] += 1

    def squish(self, humanoid):
        self.remaining_time -= ActionCost.SQUISH.value
        if not humanoid.is_zombie():
            self.__scorekeeper["killed_h"] += 1
        else:
            self.__scorekeeper["killed_z"] += 1

    def skip(self, humanoid):
        self.remaining_time -= ActionCost.SKIP.value
        if humanoid.is_injured():
            self.__scorekeeper["killed_h"] += 1

    def scram(self):
        self.remaining_time -= ActionCost.SCRAM.value
        if self.__ambulance["zombie"] > 0:
            self.__scorekeeper["killed_h"] += self.__ambulance["injured"] + self.__ambulance["healthy"]
        else:
            self.__scorekeeper["saved_h"] += self.__ambulance["injured"] + self.__ambulance["healthy"]

        self.__ambulance["zombie"] = 0
        self.__ambulance["injured"] = 0
        self.__ambulance["healthy"] = 0

    def get_current_capacity(self):
        return sum(self.__ambulance.values())

    def at_capacity(self):
        return sum(self.__ambulance.values()) >= self.__capacity

    def get_score(self):
        self.scram()
        return self.__scorekeeper
