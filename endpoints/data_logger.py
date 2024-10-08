import csv
import json
from datetime import datetime
import os
from enum import Enum
from setup import ROUNDS_PLAYED_BEFORE, CONFIG

class LoggerMode(Enum):
    RL = "rl"
    HUMAN = "human"
    MANUAL_AGENT = "manual_testing"


class DataLogger(object):
    def __init__(self, observation_fields: list, res_fields: list, config: dict, mode=LoggerMode.RL.value, folder_name=None):
        assert mode in [m.value for m in LoggerMode]
        self.mode = mode

        # Set up file structure
        if folder_name is None:
            now = datetime.now()
            folder_name = "{datetime}_log".format(datetime=now.strftime("%Y-%m-%d_%H.%M.%S"))

        os.mkdir(os.path.join("logs", mode, folder_name))

        actions_file_name = "actions.csv"
        actions_filepath = os.path.join("logs", mode, folder_name, actions_file_name)

        results_file_name = "results.csv"
        results_filepath = os.path.join("logs", mode, folder_name, results_file_name)
        
        self.actions_file = open(actions_filepath, 'w+', newline='')
        self.results_file = open(results_filepath, 'w+')

        # Set up csv file
        fieldnames = list(observation_fields)
        fieldnames.insert(0, "iteration")
        fieldnames.append('action')
        self.actions_writer = csv.DictWriter(self.actions_file, fieldnames=fieldnames)
        self.actions_writer.writeheader()

        res_fieldnames = list(res_fields)
        res_fieldnames.insert(0, "iteration")
        self.results_writer = csv.DictWriter(self.results_file, fieldnames=res_fieldnames)
        self.results_writer.writeheader()

        # set up config
        self._config_filepath = os.path.join("logs", mode, folder_name, "config.json")
        if config is not None:
            self.write_setup_file(config)

    def write_setup_file(self, config):
        if self.mode == LoggerMode.HUMAN.value:
            config.update(CONFIG)

        config_file = open(self._config_filepath, 'w+')
        json_object = json.dumps(config, indent=4)
        config_file.write(json_object)
        config_file.close()

    def log_action(self, iteration: int, action_str: str, observation: dict):
        row_dict = observation
        row_dict['action'] = action_str
        row_dict['iteration'] = iteration

        if self.mode == LoggerMode.HUMAN.value:
            row_dict['iteration'] = iteration + ROUNDS_PLAYED_BEFORE

        self.actions_writer.writerow(row_dict)

    def log_results(self, iteration: int, results: dict):
        row_dict = results
        row_dict['iteration'] = iteration
        self.results_writer.writerow(results)

    def close(self):
        self.actions_file.close()
        self.results_file.close()
