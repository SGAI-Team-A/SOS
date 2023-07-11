"""
Working Zombie versus Human Classifier!
- This a basic CNN implemented in pytorch for predicting if an image is a Human or a Zombie.
- Based on the pytorch example here: https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html
"""
import torch.nn as nn
import torch.nn.functional as F


class DefaultCNN(nn.Module):

    # Defining the Constructor
    def __init__(self, num_classes_=4):
        # In the init function, we define each layer we will use in our model
        super(DefaultCNN, self).__init__()

        # Our images are RGB, so we have input channels = 3.
        # We will apply 12 filters in the first convolutional layer
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=12, kernel_size=2, stride=1, padding=1)

        # A second convolutional layer takes 12 input channels, and generates 24 outputs
        self.conv2 = nn.Conv2d(in_channels=12, out_channels=24, kernel_size=3, stride=1, padding=1)

        # We in the end apply max pooling with a kernel size of 2
        self.pool = nn.MaxPool2d(kernel_size=2)

        # A drop layer deletes 20% of the features to help prevent overfitting
        self.drop = nn.Dropout2d(p=0.2)

        # Our 512x512 image tensors will be pooled twice with a kernel size of 2. 512/2/2 is 128  32.
        # This means that our feature tensors are now 128 x 128, and we've generated 24 of them
        # We need to flatten these in order to feed them to a fully-connected layer
        self.fc = nn.Linear(in_features=128 * 128 * 24, out_features=num_classes_)

    def forward(self, x):
        # In the forward function, pass the data through the layers we defined in the init function

        # Use a ReLU activation function after layer 1 (convolution 1 and pool)
        x = F.relu(self.pool(self.conv1(x)))

        # Use a ReLU activation function after layer 2
        x = F.relu(self.pool(self.conv2(x)))

        # Select some features to drop to prevent overfitting (only drop during training)
        x = F.dropout(self.drop(x), training=self.training)

        # Flatten
        x = x.view(-1, 128 * 128 * 24)
        # Feed to fully-connected layer to predict class

        x = self.fc(x)
        return x
