import os
from endpoints.data_parser import DataParser
from endpoints.data_logger import DataLogger
from rl_training.game_environment import GameEnv
from tqdm import tqdm

from rl_training.manual_agent import ManualAgent

data_fp = os.getenv("SGAI_DATA", default=os.path.join('data', 'test_dataset'))
data_parser = DataParser(data_fp)

FOLDER_NAME = "15_occupation_bound_ib0_sb9"

env = GameEnv(data_parser)

for doctor_bound in range(0, 11):
    for engineer_bound in range(0, 11):
        env.reset()

        config = {
            'n_episodes': 100,
            'doctor_bound': doctor_bound,
            'engineer_bound': engineer_bound
        }

        data_logger = DataLogger(
            mode="manual_testing",
            observation_fields=env.get_observation_fields(),
            res_fields=env.get_results_fields(),
            config=config,
            folder_name=os.path.join(FOLDER_NAME, "db{}_eb{}".format(config['doctor_bound'], config['engineer_bound']))
        )

        n_episodes = config['n_episodes']

        agent = ManualAgent(
            env=env,
            doctor_bound=config['doctor_bound'],
            engineer_bound=config['engineer_bound']
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
            # print(env.scorekeeper.get_scorekeeper())
        data_logger.close()
env.close()
