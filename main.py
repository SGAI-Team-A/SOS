import argparse
import os
from endpoints.data_parser import DataParser
from endpoints.machine_interface import MachineInterface
from gameplay.scorekeeper import ScoreKeeper
from gameplay.ui import UI


class Main(object):
    """
    Base class for the SGAI 2023 game
    """
    def __init__(self, is_automode, is_disable):
        self.data_fp = os.getenv("SGAI_DATA", default=os.path.join('data', 'default_dataset'))
        self.data_parser = DataParser(self.data_fp)

        self.scorekeeper = ScoreKeeper(self.data_parser.shift_length, self.data_parser.capacity)

        if not is_automode:  # Launch UI gameplay
            self.ui = UI(self.data_parser, self.scorekeeper, self.data_fp, is_disable)
        else:  # Run in background until all humanoids are processed
            simon = MachineInterface(None, None, None, is_automode)
            while len(self.data_parser.unvisited) > 0:
                if self.scorekeeper.remaining_time <= 0:
                    pass
                else:
                    humanoid = self.data_parser.get_random()
                    simon.suggest(humanoid)
                    simon.act(self.scorekeeper, humanoid)
            print(self.scorekeeper.get_score())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='python3 main.py',
        description='What the program does',
        epilog='Text at the bottom of help')
    parser.add_argument('-a', '--automode', action='store_true', help='No UI, run autonomously with model suggestions')
    parser.add_argument('-d', '--disable', action='store_true', help='Disable model help')

    args = parser.parse_args()
    Main(args.automode, args.disable)
