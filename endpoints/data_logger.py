import csv
import math
from datetime import datetime
import os

class DataLogger(object):
    def __init__(self, iteration, max_iter, mode="rl", env=None):
        now = datetime.now()
        folder_name = "{datetime}_log".format(datetime=now.strftime("%Y-%m-%d_%H.%M.%S"))
        zero_padding = len(str(max_iter))

        actions_file_name = "{iteration}_actions".format(iteration=iteration.zfill(zero_padding))
        actions_filepath = os.path.join("logs", mode, folder_name, actions_file_name)

        results_file_name = "{iteration}_res".format(iteration=iteration.zfill(zero_padding))
        results_filepath = os.path.join("logs", mode, folder_name, results_file_name)

        self.actions_file = open(actions_filepath, 'w')
        self.results_file = open(actions_filepath, 'w')

    def log_action(self, action, observation, info):
        pass
    
    def close(self):
        self.actions_file.close()
        self.results_file.close()


