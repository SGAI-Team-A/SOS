import gymnasium as gym
import numpy as np
from gymnasium import spaces

from endpoints.data_parser import DataParser
from gameplay.scorekeeper import ScoreKeeper


class GameEnv(gym.Env):
    def __init__(self, scorekeeper: ScoreKeeper, data_parser: DataParser):
        self.scorekeeper = scorekeeper
        self.data_parser = data_parser
        self.humanoid = None

        self.observation_space = spaces.Dict(
            {
                "humanoid_status": spaces.Discrete(4),
                "capacity": spaces.Discrete(11),
                "time": spaces.Discrete(145),  # 720 / 5 + 1 (all time controls are in 5 minute intervals)
            }
        )

        # 4 actions: save, scram, skip, squish
        self.action_space = spaces.Discrete(4)

    def _get_obs(self):
        return {
            "humanoid_status": self.humanoid.get_state(),
            "capacity": self.scorekeeper.get_current_capacity(),
            "time": self.scorekeeper.get_remaining_time()
        }

    def _get_info(self):
        return None  # No extra info (maybe change later?

    def step(self, action):
        pass

    def render(self):
        pass

    def reset(self):
        pass

    def close(self):
        pass