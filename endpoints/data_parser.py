import random
import yaml
from gameplay.humanoid import Humanoid
import os


class DataParser(object):
    """
    Parses the input data photos and assigns their file locations to a dictionary for later access
    """
    def __init__(self, data_fp, num_data=50):
        self.unvisited = []
        self.visited = []
        self._build_yaml(data_fp, num_data)
        i = 0
        metadata_fp = os.path.join(data_fp, "metadata.yaml")
        with open(metadata_fp, 'r') as file:
            md = yaml.safe_load(file)
            for h in md['humanoids']:
                if i >= num_data:
                    break
                filename = h["name"]
                pic_fp = os.path.join(data_fp, filename)
                if os.path.isfile(pic_fp) and pic_fp.endswith('.png'):
                    self.unvisited.append(Humanoid(h["name"], h["state"], h["value"]))
                    i += 1
            self.shift_length = md['shift_length']
            self.capacity = md['capacity']

    @staticmethod
    def _build_yaml(data_fp, max_num_data=50):
        shift_length = 720
        capacity = 10
        classes_values = {'corpse': [0], 'healthy': [1, 2, 5, 10], 'injured': [1, 2, 5, 10], 'zombie': [0]}
        humanoid_list = []
        # assumes each class has a directory within a dataset (and no other dirs exist)
        for path_ in os.listdir(data_fp):
            if os.path.isdir(os.path.join(data_fp, path_)):
                class_str = path_
                class_val_options = classes_values.get(class_str, [0])
                class_val = random.choice(class_val_options)
                for img_file_path in os.listdir(os.path.join(data_fp, path_)):
                    pic_dict = {'name': os.path.join(path_, img_file_path),
                                'state': class_str, 'value': class_val}
                    humanoid_list.append(pic_dict)

        # filter humanoid list to the maximum number of images
        # if the available humanoids is more than the max available, sample without replacement
        # otherwise, sample with replacement so that you still get the desired num of images
        if len(humanoid_list) > max_num_data:
            humanoid_list_filtered = random.sample(humanoid_list, k=max_num_data)  # without replacement
        else:
            humanoid_list_filtered = random.choices(humanoid_list, k=max_num_data)  # with replacement
        assert(len(humanoid_list_filtered) == max_num_data)

        # make full dictionary and export into the yaml file
        md_dict = {'shift_length': shift_length, 'capacity': capacity, 'humanoids': humanoid_list_filtered}
        with open(os.path.join(data_fp, "metadata.yaml"), 'w') as f_:
            yaml.dump(md_dict, f_)

    def get_random(self):
        if len(self.unvisited) == 0:
            raise ValueError("No humanoids remain")
        index = random.randint(0, (len(self.unvisited)-1))  # Technically semirandom
        humanoid = self.unvisited.pop(index)
        self.visited.append(humanoid)
        return humanoid
