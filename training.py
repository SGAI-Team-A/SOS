import os
from endpoints.data_parser import DataParser
from rl_training.game_environment import GameEnv
from gymnasium.wrappers import FlattenObservation
from rl_training.agent import GameAgent
from tqdm import tqdm

data_fp = os.getenv("SGAI_DATA", default=os.path.join('..', 'data', 'test_dataset'))
data_parser = DataParser(data_fp)

env = FlattenObservation(GameEnv(data_parser))
observation, info = env.reset()

learning_rate = 0.01
n_episodes = 100_000
start_epsilon = 1.0
epsilon_decay = start_epsilon / (n_episodes / 2)  # reduce the exploration over time
final_epsilon = 0.1

agent = GameAgent(
    env=env,
    learning_rate=learning_rate,
    initial_epsilon=start_epsilon,
    epsilon_decay=epsilon_decay,
    final_epsilon=final_epsilon,
)

for episode in tqdm(range(n_episodes)):
    obs, info = env.reset()
    done = False

    # play one episode
    while not done:
        action = agent.get_action(obs)
        next_obs, reward, terminated, truncated, info = env.step(action)

        # update the agent
        agent.update(obs, action, reward, terminated, next_obs)

        # update if the environment is done and the current obs
        done = terminated or truncated
        obs = next_obs

    if episode % 1000 == 0:
        print(env.scorekeeper.get_scorekeeper())
        print(len(env.data_parser.unvisited))

    agent.decay_epsilon()

# for _ in range(1000):
#     action = env.action_space.sample()
#     observation, reward, terminated, truncated, info = env.step(action)
#
#     if terminated or truncated:
#         observation, info = env.reset()


env.close()