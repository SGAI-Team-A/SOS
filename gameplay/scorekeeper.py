from gameplay.enums import ActionCost


class ScoreKeeper(object):
    def __init__(self, shift_len, capacity):
        self.__ambulance = {
            "zombie": 0,
            "injured": 0,
            "healthy": 0,
            "corpse": 0
        }
        self.__scorekeeper = {
            "killed_h": 0,
            "saved_h": 0,
            "killed_z" : 0,
            "saved_z" : 0
        }
        self.__capacity = capacity
        self.remaining_time = int(shift_len)  # minutes

        self.last_picked = None
        assert self.last_picked in {None, "healthy", "zombie", "injured", "corpse"}

    def save(self, humanoid):
        self.remaining_time -= ActionCost.SAVE.value
        if humanoid.is_zombie() or humanoid.is_infected():
            self.__ambulance["zombie"] += 1
            self.__scorekeeper["saved_z"] += 1

            # Immediately kill injured and healthy
            self.__scorekeeper["killed_h"] += self.__ambulance["injured"] + self.__ambulance["healthy"]

            # Remove those killed and the zombie from the van
            self.__ambulance["zombie"] = 0
            self.__ambulance["injured"] = 0
            self.__ambulance["healthy"] = 0
            self.__ambulance["corpse"] = 0

            self.last_picked = "zombie"
            
        elif humanoid.is_injured():
            self.__ambulance["injured"] += 1
            self.last_picked = "injured"
        elif humanoid.is_corpse():
            self.__ambulance["corpse"] += 1
            self.last_picked = "corpse"
        else:
            self.__ambulance["healthy"] += 1
            self.last_picked = "healthy"

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
        self.__scorekeeper["saved_h"] += self.__ambulance["injured"] + self.__ambulance["healthy"]
        self.__scorekeeper["saved_z"] += self.__ambulance["corpse"]

        self.__ambulance["zombie"] = 0
        self.__ambulance["injured"] = 0
        self.__ambulance["healthy"] = 0
        self.__ambulance["corpse"] = 0

    def get_current_capacity(self):
        return sum(self.__ambulance.values())
    
    def get_last_saved(self):
        return self.last_picked

    def at_capacity(self):
        return sum(self.__ambulance.values()) >= self.__capacity

    def get_score(self):
        self.scram()
        return self.__scorekeeper
