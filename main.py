import argparse
import os
from endpoints.data_logger import DataLogger, LoggerMode
from endpoints.data_parser import DataParser
from gameplay.scorekeeper import ScoreKeeper
from gameplay.ui import UI

class Main(object):
    """
    Base class for the SGAI 2023 game
    """
    def __init__(self, is_automode, is_disable):
        self.data_fp = os.getenv("SGAI_DATA", default=os.path.join('data', 'test_dataset'))
        self.data_parser = DataParser(self.data_fp)
        self.scorekeeper = ScoreKeeper(self.data_parser.shift_length, self.data_parser.capacity)
        self.data_logger = DataLogger(
            ["state", "occupation", "age", "gender", "name", 'capacity', 'time', 'cures'],
            self.scorekeeper.get_score(),
            config={},
            mode=LoggerMode.HUMAN.value
        )
        self.ui = UI(self.data_parser, self.scorekeeper, self.data_fp, self.data_logger, is_disable)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='python3 main.py',
        description='What the program does',
        epilog='Text at the bottom of help')
    parser.add_argument('-a', '--automode', action='store_true', help='No UI, run autonomously with model suggestions')
    parser.add_argument('-d', '--disable', action='store_true', help='Disable model help')

    args = parser.parse_args()
    Main(args.automode, args.disable)
