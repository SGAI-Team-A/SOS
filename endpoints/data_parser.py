import random
import yaml
from gameplay.humanoid import Humanoid
from gameplay.enums import State, Occupation
import os
import numpy as np


class DataParser(object):
    """
    Parses the input data photos and assigns their file locations to a dictionary for later access
    """

    def __init__(self, data_fp, num_data=144):
        self.data_fp = data_fp
        self.num_data = num_data

        self._init_humanoids_and_probabilities()  # only needs to be called once
        self.reset_game()

    def reset_game(self, use_metadata=True):
        self.unvisited = []
        self.visited = []

        if use_metadata:
            self._build_yaml(self.data_fp)
            i = 0
            metadata_fp = os.path.join(self.data_fp, "metadata.yaml")
            with open(metadata_fp, 'r') as file:
                md = yaml.safe_load(file)
                for h in md['humanoids']:
                    if i >= self.num_data:
                        break
                    filename = h["name"]
                    pic_fp = os.path.join(self.data_fp, filename)
                    if os.path.isfile(pic_fp) and pic_fp.endswith('.png'):
                        self.unvisited.append(Humanoid(h["name"], h["state"], h["occupation"], h["age"], h["gender"]))
                        i += 1
                self.shift_length = md['shift_length']
                self.capacity = md['capacity']
        else:
            data = self._get_data()
            i = 0
            self.capacity = data['capacity']
            self.shift_length = data['shift_length']
            for h in data['humanoids']:
                if i >= self.num_data:
                    break
                self.unvisited.append(Humanoid(h["name"], h["state"], h["occupation"]))
                i += 1

    def _init_humanoids_and_probabilities(self):
        # probabilities for each state when being randomly chosen
        states_probabilities = {
            State.ZOMBIE.value: 0.3,
            State.CORPSE.value: 0.1,
            State.HEALTHY.value: 0.25,
            State.INJURED.value: 0.35
        }
        assert (sum(states_probabilities.values()) == 1)

        # probabilities for each occupation when being randomly chosen
        occupation_probabilities = {
            Occupation.DOCTOR.value: 0.1,
            Occupation.ENGINEER.value: 0.1,
        }
        occupation_probabilities[Occupation.OTHER.value] = 1 - sum(occupation_probabilities.values())

        self.humanoid_list = []
        self.probability_list = []

        # assumes each class has a directory within a dataset (and no other dirs exist)
        for path_ in os.listdir(self.data_fp):
            if os.path.isdir(os.path.join(self.data_fp, path_)):
                # iterate through each of the different occupations
                for occupation_path in os.listdir(os.path.join(self.data_fp, path_)):
                    if os.path.isdir(os.path.join(self.data_fp, path_, occupation_path)):
                        state_str = path_
                        occupation_str = occupation_path

                        num_imgs = 0  # number of images in the current folder
                        for img_file_path in os.listdir(os.path.join(self.data_fp, path_, occupation_path)):
                            if img_file_path.endswith('.png'):
                                img_file_name = img_file_path[:-4]  # remove .png
                                state, gender, occupation, age, _ = img_file_name.split("_")

                                gender_to_full = {
                                    'w': "woman",
                                    'm': "man"
                                }

                                age_to_full = {
                                    'y': "young",
                                    'm': "middle",
                                    'o': "old"
                                }

                                num_imgs += 1
                                pic_dict = {
                                    'name': os.path.join(path_, occupation_path, img_file_path),
                                    'state': state_str,
                                    'occupation': occupation_str,
                                    'gender': gender_to_full[gender],
                                    'age': age_to_full[age]
                                }
                                self.humanoid_list.append(pic_dict)

                        # calculate probability of this image being drawn
                        probability = states_probabilities[state_str] * occupation_probabilities[
                            occupation_str] * (1 / num_imgs)
                        self.probability_list += [probability] * num_imgs

    def _get_data(self):
        shift_length = 720
        capacity = 10

        # filter humanoid list to the maximum number of images
        # sample with replacement to get correct probabilities
        humanoid_list_filtered = np.random.choice(
            self.humanoid_list,
            size=self.num_data,
            replace=True,
            p=self.probability_list
        )
        assert (len(humanoid_list_filtered) == self.num_data)

        # return full dictionary
        md_dict = {'shift_length': shift_length, 'capacity': capacity, 'humanoids': humanoid_list_filtered.tolist()}
        return md_dict

    def _build_yaml(self, data_fp):
        # make full dictionary and export into the yaml file
        md_dict = self._get_data()
        with open(os.path.join(data_fp, "metadata.yaml"), 'w') as f_:
            yaml.dump(md_dict, f_)

    def get_random(self):
        if len(self.unvisited) == 0:
            #raise ValueError("No humanoids remain")
            print("No humanoids remain")
        else :
            index = random.randint(0, (len(self.unvisited) - 1))  # Technically semirandom
            humanoid = self.unvisited.pop(index)
            self.visited.append(humanoid)
            return humanoid