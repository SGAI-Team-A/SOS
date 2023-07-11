from enum import Enum


class State(Enum):
    ZOMBIE = "zombie"
    HEALTHY = "healthy"
    INJURED = "injured"
    CORPSE = "corpse"


class ActionCost(Enum):
    SAVE = 30
    SQUISH = 5
    SKIP = 15
    SCRAM = 120
