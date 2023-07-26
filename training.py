import os
from endpoints.data_parser import DataParser
from endpoints.data_logger import DataLogger
from rl_training.game_environment import GameEnv
from gymnasium.wrappers import FlattenObservation
from rl_training.agent import GameAgent
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import dill as pickle
from datetime import datetime

data_fp = os.getenv("SGAI_DATA", default=os.path.join('data', 'test_dataset'))
data_parser = DataParser(data_fp)

env = FlattenObservation(GameEnv(data_parser))
observation, info = env.reset()

data_logger = DataLogger(observation_fields=env.unwrapped.get_observation_fields(), res_fields=env.unwrapped.get_results_fields())

learning_rate = 0.01
n_episodes = 100
start_epsilon = 1.0
epsilon_decay = start_epsilon / (n_episodes / 2)  # reduce the exploration over time
final_epsilon = 0.1

now = datetime.now()
model_name = "{datetime}_q-table_{n_episodes}".format(datetime=now.strftime("%Y-%m-%d_%H.%M.%S"), n_episodes = n_episodes)

agent = GameAgent(
    env=env,
    learning_rate=learning_rate,
    initial_epsilon=start_epsilon,
    epsilon_decay=epsilon_decay,
    final_epsilon=final_epsilon,
)

q_value = agent.get_q()
#loads the saved file with q-values *have to manually put in file name*
#with open(os.path.join("logs", "model", "2023-07-25_16.07.34_q-table_100000"), "rb") as f:
    #q_value = pickle.load(f)
    
for episode in tqdm(range(n_episodes)):
    obs, info = env.reset()
    done = False
    # play one episode
    while not done:
        action = agent.get_action(obs)
        data_logger.log_action(episode, env.unwrapped.action_to_str[action], env.unwrapped.get_human_readable_observation())
        next_obs, reward, terminated, truncated, info = env.step(action)

        # update the agent
        agent.update(obs, action, reward, terminated, next_obs)

        # update if the environment is done and the current obs
        done = terminated or truncated
        if done:
             data_logger.log_results(episode, env.unwrapped.get_results())
             observation, info = env.reset()
        obs = next_obs
    if episode % 1000 == 0:
        print(env.scorekeeper.get_scorekeeper())

    agent.decay_epsilon()

# for _ in range(1000):
#     action = env.action_space.sample()
#     observation, reward, terminated, truncated, info = env.step(action)
#
#     if terminated or truncated:
#         observation, info = env.reset()
#saves q-values into a file
with open(os.path.join("logs", "model", model_name), "wb") as f:
    pickle.dump(agent.get_q(), f) 
env.close()
data_logger.close()
