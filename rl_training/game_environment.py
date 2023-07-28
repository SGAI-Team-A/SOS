import gymnasium as gym
from gymnasium import spaces

from endpoints.data_parser import DataParser
from gameplay.scorekeeper import ScoreKeeper
from gameplay.enums import State, ActionCost, Action, Occupation


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
                "cures": spaces.Discrete(11),
                "humanoid_occupation": spaces.Discrete(3)
            }
        )

        # 4 actions: save, scram, skip, squish
        self.action_space = spaces.Discrete(4)

        self.action_number_to_str = [Action.SAVE.value, Action.SCRAM.value, Action.SKIP.value, Action.SQUISH.value]

        self.action_str_to_number = {
            val: index for index, val in enumerate(self.action_number_to_str)
        }

        self._humanoid_state_to_number = {
            val: index for index, val in enumerate([e.value for e in State])
        }

        self.humanoid_number_to_state = {
            val: index for index, val in self._humanoid_state_to_number.items()
        }

        self.occupation_to_number = {
            val: index for index, val in enumerate([e.value for e in Occupation])
        }

        self.number_to_occupation = {
            val: index for index, val in self.occupation_to_number.items()
        }

        self.illegal_moves = 0
        self.reward = 0

    # perform relevant function based on action number
    def _action_to_function(self, action: int):
        if not self.is_legal(action):
            # print("illegal")
            self.illegal_moves += 1
            #self.scorekeeper.set_reward(-100000)
            return

        self.scorekeeper.set_reward(0)
        # save
        if action == 0:
            self.scorekeeper.set_reward(self.scorekeeper.get_reward() - ActionCost.SAVE.value // 2)
            if self.humanoid.is_healthy() or self.humanoid.is_injured():
                self.scorekeeper.set_reward(self.scorekeeper.get_reward() + 10)
            self.scorekeeper.save(self.humanoid)
        # scram
        elif action == 1:
            self.scorekeeper.set_reward(self.scorekeeper.get_reward() - ActionCost.SCRAM.value // 2)
            self.scorekeeper.scram()
        # skip
        elif action == 2:
            self.scorekeeper.set_reward(self.scorekeeper.get_reward() - ActionCost.SKIP.value // 2)
            self.scorekeeper.skip(self.humanoid)
        # squish
        elif action == 3:
            self.scorekeeper.set_reward(self.scorekeeper.get_reward() - ActionCost.SQUISH.value // 2)
            self.scorekeeper.squish(self.humanoid)

    def is_legal(self, action: int):
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
            "time": self.scorekeeper.get_remaining_time() // 5,
            "cures": self.scorekeeper.get_cures(),
            "humanoid_occupation": self.occupation_to_number[self.humanoid.get_occupation()]
        }

    def _get_info(self):
        return None  # No extra info (maybe change later?)

    def step(self, action: int):
        self._action_to_function(action)

        reward = self.scorekeeper.get_reward()

        self.reward += reward

        #truncated = len(self.data_parser.unvisited) <= 0
        terminated = self.scorekeeper.remaining_time <= 0
        if len(self.data_parser.unvisited) <= 0:
            while self.scorekeeper.get_remaining_time() > 0:
                self.scorekeeper.scram()
            truncated = True
        else:
            truncated = False
        if terminated or truncated:
            done = True
        # if terminated or truncated:
        #     print(self.scorekeeper.get_scorekeeper())

        # select humanoid
        self.humanoid = self.data_parser.get_random()

        observation = self._get_obs()
        info = self._get_info()

        return observation, reward, terminated, truncated, info

    def render(self):
        pass

    def reset(self, seed=None, options=None):
        # seed self.np_random
        super().reset(seed=seed)

        self.reward = 0
        self.illegal_moves = 0

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
            "time": self.scorekeeper.get_remaining_time(),
            "cures": self.scorekeeper.get_cures(),
            "humanoid_occupation": self.humanoid.get_occupation()
        }

    def get_observation_fields(self) -> list:
        return list(self.get_human_readable_observation().keys())

    def get_results(self) -> dict:
        res = self.scorekeeper.get_scorekeeper()
        res['reward'] = self.reward

        return res

    def get_results_fields(self) -> list:
        fields = list(self.scorekeeper.get_scorekeeper().keys())
        fields.append("reward")
        return fields
