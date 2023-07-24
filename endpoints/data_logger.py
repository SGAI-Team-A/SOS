import csv
import math
from datetime import datetime
import os

class DataLogger(object):
    def __init__(self, iteration, max_iter, observation_fields:list, mode="rl"):
        # Set up file structure
        now = datetime.now()
        folder_name = "{datetime}_log".format(datetime=now.strftime("%Y-%m-%d_%H.%M.%S"))
        zero_padding = len(str(max_iter))

        actions_file_name = "{iteration}_actions".format(iteration=iteration.zfill(zero_padding))
        actions_filepath = os.path.join("logs", mode, folder_name, actions_file_name)

        results_file_name = "{iteration}_res".format(iteration=iteration.zfill(zero_padding))
        results_filepath = os.path.join("logs", mode, folder_name, results_file_name)

        self.actions_file = open(actions_filepath, 'w', newline='')
        self.results_file = open(results_filepath, 'w')

        # Set up csv file
        observation_fields.append('action')
        self.actions_writer = csv.DictWriter(self.actions_file, fieldnames=observation_fields)
        self.actions_writer.writeheader()

    def log_action(self, action_str:str, observation: dict):
        row_dict = observation
        row_dict['action'] = action_str

        self.actions_writer.writerow(row_dict)

    def log_results(self, results):
        pass

    def close(self):
        self.actions_file.close()
        self.results_file.close()


