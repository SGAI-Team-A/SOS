from enum import Enum

class State(Enum):
    ZOMBIE = "zombie"
    HEALTHY = "healthy"
    INJURED = "injured"
    INFECTED = "infected"
    CORPSE = "corpse"

class Occupation(Enum):
    DOCTOR = "doctor"
    ENGINEER = "engineer"
    OTHER = "other"

class ActionCost(Enum):
    SAVE = 30
    SQUISH = 5
    SKIP = 15
    SCRAM = 120

class Age(Enum):
    YOUNG = 0
    MIDDLE = 1
    OLD = 2

class Gender(Enum):
    MALE = 0
    FEMALE = 1