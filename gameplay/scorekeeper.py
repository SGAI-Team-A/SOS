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
            "killed_h_squish": 0,
            "killed_in_squish": 0,
            "killed_zombie": 0,
            "skipped_in": 0,
            "saved_h": 0,
            "saved_in": 0,
            "killed_z": 0,
            "killed_c": 0,
            "saved_z": 0,
            "saved_c": 0
        }
        self.__capacity = capacity
        self.max_time = int(shift_len)
        self.remaining_time = int(shift_len)  # minutes
        self.update = ""
        
        self.last_picked = None
        assert self.last_picked in {None, "healthy", "zombie", "injured", "corpse"}

        self.update = ""  # for human UI
        self.reward = 0  # for RL model
        
    def save(self, humanoid):
        if self.get_current_capacity() >= self.__capacity:
            return

        self.remaining_time -= ActionCost.SAVE.value
        self.update = ""
        if self.__cures > 0 and humanoid.is_injured():
            humanoid.cure(scorekeeper=self)
            self.set_update("You used one of your cures to cure an injured person!")
            self.__cures -= 1
        
        if humanoid.is_zombie() or humanoid.is_infected():
            self.__ambulance["zombie"] += 1
            self.increment_scorekeeper("saved_z", 1)
            if humanoid.is_zombie():
                if self.__ambulance["injured"] + self.__ambulance["healthy"] == 0:
                    self.update = "You saved a zombie! Fortunately, no passengers who were alive were in the van."
                else:
                    self.update = "The zombie you saved killed " + str(self.__ambulance["injured"] + self.__ambulance["healthy"]) + " people. The van is empty now."
            else:
                if self.__ambulance["injured"] + self.__ambulance["healthy"] == 0:
                    self.update = "The injured person you saved was actually infected! \nFortunately, no passengers who were alive were in the van."
                else:
                    self.update = "The infected person you saved killed " + str(self.__ambulance["injured"] + self.__ambulance["healthy"]) + " people. The van is empty now."
            
            # Immediately kill injured and healthy
            self.increment_scorekeeper("killed_zombie", self.__ambulance["injured"] + self.__ambulance["healthy"])
            # Remove those killed and the zombie from the van
            self.last_picked = "zombie"
            self.empty_ambulance()
            
        elif humanoid.is_injured():
            self.__ambulance["injured"] += 1
            self.last_picked = "injured"
            humanoid.perform_action(scorekeeper=self)

        elif humanoid.is_corpse():
            self.__ambulance["corpse"] += 1
            self.last_picked = "corpse"
            self.update = "You saved a corpse, one less space on the \nvan that could have been used for others."

        else:
            self.__ambulance["healthy"] += 1
            self.last_picked = "healthy"
            humanoid.perform_action(scorekeeper=self)

    def squish(self, humanoid):
        self.remaining_time -= ActionCost.SQUISH.value
        if humanoid.is_zombie():
            self.increment_scorekeeper("killed_z", 1)
            self.update = ""
        elif humanoid.is_corpse():
            self.increment_scorekeeper("killed_c", 1)
            self.update = ""
        else:
            if humanoid.is_injured():
                self.increment_scorekeeper("killed_in_squish", 1)
            else:
                self.increment_scorekeeper("killed_h_squish", 1)
            self.update = "You killed a human!"
            
    def skip(self, humanoid):
        self.update = ""
        self.remaining_time -= ActionCost.SKIP.value
        if humanoid.is_injured():
            self.__scorekeeper["skipped_in"] += 1

    def scram(self):
        self.update = ""
        self.remaining_time -= ActionCost.SCRAM.value

        # Update score
        self.increment_scorekeeper("saved_h", self.__ambulance["healthy"])
        self.increment_scorekeeper("saved_in", self.__ambulance["injured"])
        self.increment_scorekeeper("saved_c", self.__ambulance["corpse"])
        self.empty_ambulance()
    
    def get_update(self):
        return self.update

    def gain_battery(self):
        if self.remaining_time < self.max_time:
            self.remaining_time += min(60, self.max_time - self.remaining_time)

    def gain_cure(self):
        self.__cures += 1

    def get_cures(self):
        return self.__cures

    def get_current_capacity(self):
        return sum(self.__ambulance.values())
    
    def get_last_saved(self):
        return self.last_picked

    def get_remaining_time(self):
        return self.remaining_time

    def at_capacity(self):
        return sum(self.__ambulance.values()) >= self.__capacity

    def get_score(self):
        return self.__scorekeeper
    
    def empty_ambulance(self):
        for category in self.__ambulance.keys():
            self.__ambulance[category] = 0
        self.__cures = 0 # reset cures when emptied

    def set_update(self, update):
        self.update = update

    def set_reward(self, reward):
        self.reward = reward

    def get_reward(self):
        return self.reward

    # handles whenever you want to adjust self.__scorekeeper
    # add to current amount (if you need to subtract, make amount negative)
    # handles rewards based on scorekeeper
    def increment_scorekeeper(self, key, amount):
        self.__scorekeeper[key] += amount

        if key == "killed_h_squish":
            self.set_reward(self.get_reward() - amount*10)
        if key == "killed_zombie":
            self.set_reward(self.get_reward() - amount*10)
        if key == "saved_h":
            self.set_reward(self.get_reward() + amount*10)
        if key == "saved_in":
            self.set_reward(self.get_reward() + amount*10)
        if key == "saved_z":
            self.set_reward(self.get_reward() - amount*10)
        if key == "saved_c":
            self.set_reward(self.get_reward() - amount*10)
        
    def get_scorekeeper(self):
        return self.__scorekeeper
    
    def get_cures(self):
        return self.__cures
