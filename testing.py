import os
from endpoints.data_parser import DataParser
from endpoints.data_logger import DataLogger
from rl_training.game_environment import GameEnv
from tqdm import tqdm

from rl_training.manual_agent import ManualAgent

data_fp = os.getenv("SGAI_DATA", default=os.path.join('data', 'test_dataset'))
data_parser = DataParser(data_fp)

env = GameEnv(data_parser)
env.reset()

config = {
    'n_episodes': 100,
    'injured_bound': 5,
    'scram_bound': 10
}

data_logger = DataLogger(
    mode="manual_testing",
    observation_fields=env.get_observation_fields(),
    res_fields=env.get_results_fields(),
    config=config
)

n_episodes = config['n_episodes']

agent = ManualAgent(
    env=env,
    injured_bound=config['injured_bound'],
    scram_bound=config['scram_bound']
)

for episode in tqdm(range(n_episodes)):
    obs, info = env.reset()
    done = False
    # play one episode
    while not done:
        action = agent.get_action(obs)
        data_logger.log_action(episode, env.action_number_to_str[action], env.get_human_readable_observation())
        next_obs, reward, terminated, truncated, info = env.step(action)

        # update if the environment is done and the current obs
        done = terminated or truncated
        if done:
            data_logger.log_results(episode, env.get_results())
        obs = next_obs
    print(env.scorekeeper.get_scorekeeper())

env.close()
data_logger.close()
