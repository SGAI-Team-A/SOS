import os
import math
import random
import tkinter as tk
from PIL import Image
import torch
from torchvision import transforms

from gameplay.enums import ActionCost, State
from models.DefaultCNN import DefaultCNN


class MachineInterface(object):
    def __init__(self, root, w, h, is_automode=False, model_file=os.path.join('models', 'default.pth'),
                 img_data_root=os.path.join('data', 'default_dataset')):
        self.text = ""
        self.is_automode = is_automode
        self.img_data_root = img_data_root

        # load model
        self.net = None
        self.is_model_loaded: bool = self._load_model(model_file)

        if not self.is_automode:
            self.canvas = tk.Canvas(root, width=math.floor(0.2 * w), height=math.floor(0.1 * h))
            self.canvas.place(x=math.floor(0.75 * w), y=math.floor(0.75 * h))
            self.label = tk.Label(self.canvas, text="Simon says...", font=("Arial", 20))
            self.label.pack(side=tk.TOP)

            self.suggestion = tk.Label(self.canvas, text=self.text, font=("Arial", 20))
            self.suggestion.pack(side=tk.TOP)

    def _load_model(self, weights_path, num_classes=4):
        try:
            self.net = DefaultCNN(num_classes)
            self.net.load_state_dict(torch.load(weights_path))
            return True
        except:  # file not found, maybe others?
            return False

    def suggest(self, humanoid, capacity_full=False):
        if self.is_model_loaded:
            action = self.get_model_suggestion(humanoid, capacity_full)
        else:
            action = self.get_random_suggestion()
        self.text = action.name
        if not self.is_automode:
            self.suggestion.config(text=self.text)

    def act(self, scorekeeper, humanoid):
        action = self.text
        if action == ActionCost.SKIP.name:
            scorekeeper.skip(humanoid)
        elif action == ActionCost.SQUISH.name:
            scorekeeper.squish(humanoid)
        elif action == ActionCost.SAVE.name:
            scorekeeper.save(humanoid)
        elif action == ActionCost.SCRAM.name:
            scorekeeper.scram()
        else:
            raise ValueError("Invalid action suggested")

    @staticmethod
    def get_random_suggestion():
        return random.choice(list(ActionCost))

    def get_model_suggestion(self, humanoid, is_capacity_full) -> ActionCost:
        # Working Zombie versus Human Classifier!
        # - This a basic CNN implemented in pytorch for predicting if an image is a Human or a Zombie.
        # - Based on the pytorch example here: https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html
        image_loader = transforms.Compose([transforms.ToTensor()])
        img_ = Image.open(os.path.join(self.img_data_root, humanoid.fp))
        img_ = image_loader(img_).float()
        img_ = img_.unsqueeze(0)

        self.net.eval()
        with torch.no_grad():
            # calculate outputs by running images through the network
            outputs = self.net(img_)
            # the class with the highest energy is what we choose as prediction
            _, predicted = torch.max(outputs.data, 1)
            class_strings = ['corpse', 'healthy', 'injured', 'zombie']
            class_string = class_strings[predicted.item()]
            predicted_state = State(class_string)

        # given the model's class prediction, recommend an action
        recommended_action = self._map_class_to_action_default(predicted_state, is_capacity_full)
        return recommended_action

    @staticmethod
    def _map_class_to_action_default(predicted_state: State, is_capacity_full: bool = False) -> ActionCost:
        # map prediction to ActionCost to return the right thing; now aligned with Rob's pseudocode
        if is_capacity_full:
            return ActionCost.SCRAM
        if predicted_state is State.ZOMBIE:
            return ActionCost.SQUISH
        if predicted_state is State.INJURED:
            return ActionCost.SAVE
        if predicted_state is State.HEALTHY:
            return ActionCost.SAVE
        if predicted_state is State.CORPSE:
            return ActionCost.SQUISH
