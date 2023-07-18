from gameplay.enums import ActionCost


class ScoreKeeper(object):
    def __init__(self, shift_len, capacity):
        self.__ambulance = {
            "zombie": 0,
            "injured": 0,
            "healthy": 0,
            "corpse": 0
        }
        self.__cures = 0
        self.__scorekeeper = {
            "killed_h": 0,
            "saved_h": 0,
            "killed_z": 0,
            "saved_z": 0
        }
        self.__capacity = capacity
        self.remaining_time = int(shift_len)  # minutes

    def save(self, humanoid):
        self.remaining_time -= ActionCost.SAVE.value

        if self.__cures > 0 and humanoid.is_injured():
            humanoid.cure(scorekeeper=self)
            self.__cures -= 1

        if humanoid.is_zombie() or humanoid.is_infected():
            self.__ambulance["zombie"] += 1
            self.__scorekeeper["saved_z"] += 1

            # Immediately kill injured and healthy
            self.__scorekeeper["killed_h"] += self.__ambulance["injured"] + self.__ambulance["healthy"]

            self.empty_ambulance()
        elif humanoid.is_injured():
            self.__ambulance["injured"] += 1
        elif humanoid.is_corpse():
            self.__ambulance["corpse"] += 1
        else:
            self.__ambulance["healthy"] += 1
            humanoid.perform_action(scorekeeper=self)

    def squish(self, humanoid):
        self.remaining_time -= ActionCost.SQUISH.value
        if humanoid.is_zombie() or humanoid.is_corpse():
            self.__scorekeeper["killed_z"] += 1
        else:
            self.__scorekeeper["killed_h"] += 1

    def skip(self, humanoid):
        self.remaining_time -= ActionCost.SKIP.value
        if humanoid.is_injured():
            self.__scorekeeper["killed_h"] += 1

    def scram(self):
        self.remaining_time -= ActionCost.SCRAM.value

        # Update score
        self.__scorekeeper["saved_h"] += self.__ambulance["injured"] + self.__ambulance["healthy"]
        self.__scorekeeper["saved_z"] += self.__ambulance["corpse"]

        self.empty_ambulance()

    def gain_battery(self):
        self.remaining_time += 60

    def gain_cure(self):
        self.__cures += 1

    def get_current_capacity(self):
        return sum(self.__ambulance.values())

    def at_capacity(self):
        return sum(self.__ambulance.values()) >= self.__capacity

    def get_score(self):
        self.scram()
        return self.__scorekeeper

    def empty_ambulance(self):
        for category in self.__ambulance.keys():
            self.__ambulance[category] = 0
