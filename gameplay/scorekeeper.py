from gameplay.enums import ActionCost
from ui_elements.update_log import UpdateLog
from gameplay.ui import UI

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

    def save(self, humanoid):
        self.remaining_time -= ActionCost.SAVE.value
        self.update = ""
        if humanoid.is_zombie() or humanoid.is_infected():
            self.__ambulance["zombie"] += 1
            self.__scorekeeper["saved_z"] += 1
            if humanoid.is_zombie():
                if sum(self.__ambulance.values()) == 1:
                    self.update = "You saved a zombie! Fortunately, no passengers were in the van."
                else:
                    self.update = "The zombie you saved killed " + str(sum(self.__ambulance.values())-1) + " number of people. The van is empty now."
            else:
                if sum(self.__ambulance.values()) == 1:
                    self.update = "The injured person you saved was actually infected! Fortunately, no passengers were in the van."
                else:
                    self.update = "The infected person you saved killed " + str(sum(self.__ambulance.values())-1) + " number of people. The van is empty now."
            
            # Immediately kill injured and healthy
            self.__scorekeeper["killed_h"] += self.__ambulance["injured"] + self.__ambulance["healthy"]

            # Remove those killed and the zombie from the van
            self.__ambulance["zombie"] = 0
            self.__ambulance["injured"] = 0
            self.__ambulance["healthy"] = 0
            self.__ambulance["corpse"] = 0

        elif humanoid.is_injured():
            self.__ambulance["injured"] += 1
        elif humanoid.is_corpse():
            self.__ambulance["corpse"] += 1
            self.update = "You saved a corpse, one less space on the van that could have been used for others."
        else:
            self.__ambulance["healthy"] += 1
        UpdateLog(self.update, UI.canvas)
         
    def squish(self, humanoid):
        self.remaining_time -= ActionCost.SQUISH.value
        if not humanoid.is_zombie() or not humanoid.is_corpse():
            self.__scorekeeper["killed_h"] += 1
            update = "You killed a human!"
            UpdateLog(self.update, UI.canvas)
        else:
            self.__scorekeeper["killed_z"] += 1
        
    def skip(self, humanoid):
        self.remaining_time -= ActionCost.SKIP.value
        if humanoid.is_injured():
            self.__scorekeeper["killed_h"] += 1
        self.update =""
        UpdateLog(self.update, UI.canvas)
        
    def scram(self):
        self.remaining_time -= ActionCost.SCRAM.value
        self.__scorekeeper["saved_h"] += self.__ambulance["injured"] + self.__ambulance["healthy"]
        self.__scorekeeper["saved_z"] += self.__ambulance["corpse"]

        self.__ambulance["zombie"] = 0
        self.__ambulance["injured"] = 0
        self.__ambulance["healthy"] = 0
        self.__ambulance["corpse"] = 0
        self.update =""
        UpdateLog(self.update, UI.canvas)
        
    def get_current_capacity(self):
        return sum(self.__ambulance.values())

    def at_capacity(self):
        return sum(self.__ambulance.values()) >= self.__capacity

    def get_score(self):
        self.scram()
        return self.__scorekeeper
