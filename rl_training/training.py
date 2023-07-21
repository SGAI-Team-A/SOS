import os
from endpoints.data_parser import DataParser
from game_environment import GameEnv

data_fp = os.getenv("SGAI_DATA", default=os.path.join('..', 'data', 'test_dataset'))
data_parser = DataParser(data_fp)

env = GameEnv(data_parser)
observation, info = env.reset()

for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)

    if terminated or truncated:
        observation, info = env.reset()


env.close()