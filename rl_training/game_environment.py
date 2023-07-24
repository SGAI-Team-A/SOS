import gymnasium as gym
from gymnasium import spaces

from endpoints.data_parser import DataParser
from gameplay.scorekeeper import ScoreKeeper
from gameplay.enums import State, ActionCost

class GameEnv(gym.Env):
    def __init__(self, data_parser: DataParser):
        self.data_parser = data_parser
        self.scorekeeper = ScoreKeeper(self.data_parser.shift_length, self.data_parser.capacity)
        self.humanoid = None

        self.observation_space = spaces.Dict(
            {
                "humanoid_status": spaces.Discrete(5),
                "capacity": spaces.Discrete(11),
                "time": spaces.Discrete(145),  # 720 / 5 + 1 (all time controls are in 5 minute intervals)
            }
        )

        # 4 actions: save, scram, skip, squish
        self.action_space = spaces.Discrete(4)

        self.action_to_str = ["save", "scram", "skip", "squish"]

        self._humanoid_state_to_number = {
            val: index for index, val in enumerate([e.value for e in State])
        }

    # perform relevant function based on action number
    def _action_to_function(self, action):
        if not self.is_legal(action):
            return

        self.scorekeeper.set_reward(0)
        if action == 0:
            self.scorekeeper.save(self.humanoid)
        elif action == 1:
            self.scorekeeper.scram()
        elif action == 2:
            self.scorekeeper.skip(self.humanoid)
        elif action == 3:
            self.scorekeeper.squish(self.humanoid)

    def is_legal(self, action):
        # save
        if action == 0:
            return not self.scorekeeper.at_capacity() and \
                self.scorekeeper.remaining_time - ActionCost.SAVE.value >= ActionCost.SCRAM.value
        # scram
        elif action == 1:
            return True
        # skip
        elif action == 2:
            return self.scorekeeper.remaining_time - ActionCost.SKIP.value >= ActionCost.SCRAM.value
        # squish
        elif action == 3:
            return self.scorekeeper.remaining_time - ActionCost.SQUISH.value >= ActionCost.SCRAM.value

    def _get_obs(self):
        return {
            "humanoid_status": self._humanoid_state_to_number[self.humanoid.get_state()],
            "capacity": self.scorekeeper.get_current_capacity(),
            "time": self.scorekeeper.get_remaining_time() // 5
        }

    def _get_info(self):
        return None  # No extra info (maybe change later?)

    def step(self, action):
        self._action_to_function(action)

        reward = self.scorekeeper.get_reward()

        truncated = len(self.data_parser.unvisited) <= 0
        terminated = self.scorekeeper.remaining_time <= 0

        # if terminated or truncated:
        #     print(self.scorekeeper.get_scorekeeper())

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, truncated, info

    def render(self):
        pass

    def reset(self, seed=None, options=None):
        # seed self.np_random
        super().reset(seed=seed)

        # select new random set of images
        self.data_parser.reset_game()

        # reset scorekeeper
        self.scorekeeper = ScoreKeeper(self.data_parser.shift_length, self.data_parser.capacity)

        # select first humanoid
        self.humanoid = self.data_parser.get_random()

        observation = self._get_obs()
        info = self._get_info()

        return observation, info

    def close(self):
        pass

    def get_human_readable_observation(self):
        return {
            "humanoid_status": self.humanoid.get_state(),
            "capacity": self.scorekeeper.get_current_capacity(),
            "time": self.scorekeeper.get_remaining_time()
        }

    def get_observation_fields(self) -> list:
        return list(self.get_human_readable_observation().keys())

    def get_results(self) -> dict:
        return self.scorekeeper.get_scorekeeper()

    def get_results_fields(self) -> list:
        return list(self.scorekeeper.get_scorekeeper().keys())