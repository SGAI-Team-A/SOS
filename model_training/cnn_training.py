# Working Zombie versus Human Classifier!
# - This a basic CNN implemented in pytorch for predicting if an image is a Human or a Zombie.
# - Will be transitioning to a 4 class model soon
# - Based on the pytorch example here:
#   https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html

## Imports and Inputs
import os
import numpy as np
import matplotlib.pyplot as plt
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch
import torchvision
# for plotting and stuff
from sklearn.metrics import confusion_matrix
import seaborn as sn
import pandas as pd

print(torch.__version__)

## Loading / Preprocessing Data
tf_a = transforms.Compose([transforms.ToTensor()])



# For full data set
# name_ = 'full'
# data_dir = os.path.join('data', 'full_data')
# train_set = datasets.ImageFolder(os.path.join(data_dir, 'training_set_a'), transform=tf_a)
# test_set = datasets.ImageFolder(os.path.join(data_dir, 'test_set_a'), transform=tf_a)

# For loading the poor data stes
data_dir = os.path.join('data', 'poor_data')
name_ = 'bifurcate'
# name_ = 'noisy'
# name_ = 'rotate'
# name_ = 'starved'
# name_ = 'unballanced'
train_set = datasets.ImageFolder(os.path.join(data_dir, f'training_set_{name_}'), transform=tf_a)
test_set = datasets.ImageFolder(os.path.join(data_dir, f'test_set_{name_}'), transform=tf_a)

# Load the data
batch_size = 32
train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=True)

# The training and test set are built and labels inferred. We set these values, so we can
# decode them easily. Note: The order of class labels should be the same alphabetical
# order as the class subdirectories in the data set directory.

class_labels = ('corpse', 'healthy', 'injured', 'zombie')  # Defining the classes we have
num_classes = len(class_labels)


## Defining CNN
# Create a neural net class
class Net(nn.Module):

    # Defining the Constructor
    def __init__(self, num_classes_=4):
        # In the init function, we define each layer we will use in our model
        super(Net, self).__init__()

        # Our images are RGB, so we have input channels = 3.
        # We will apply 12 filters in the first convolutional layer
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=12, kernel_size=2, stride=1, padding=1)

        # A second convolutional layer takes 12 input channels, and generates 24 outputs
        self.conv2 = nn.Conv2d(in_channels=12, out_channels=24, kernel_size=3, stride=1, padding=1)

        # We in the end apply max pooling with a kernel size of 2
        self.pool = nn.MaxPool2d(kernel_size=2)

        # A drop layer deletes 20% of the features to help prevent overfitting
        self.drop = nn.Dropout2d(p=0.2)

        # Our 512x512 image tensors will be pooled twice with a kernel size of 2. 512/2/2 is 128
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


net = Net(num_classes)
print(net)


## Training
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=0.001, weight_decay=0)  # what is lr and weight_decay?

loss_vals = []  # capture these values for plotting

num_epochs = 25  # 25 is a good place to start for pretty good performance, experiment with different values
for epoch in range(num_epochs):  # loop over the dataset multiple times

    for i, data in enumerate(train_loader, 0):
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # logging
        loss_vals.append(loss.item())
        print(f'epoch: {epoch:2d} - batch: {i:3d} - loss: {loss.item():.5f}')

print('Finished Training')


## Save out and/or load model
PATH = os.path.join('outputs', f'{name_}_net.pth')
torch.save(net.state_dict(), PATH)


## Evaluate

# Plot the loss to see how well it trained (usually the first step)
plt.plot(loss_vals)
plt.yscale('log')
# plt.show()


### Metrics

correct = 0
total = 0
net.eval()
# since we're not training, we don't need to calculate the gradients for our outputs
with torch.no_grad():
    for data in test_loader:  # test_loader:
        images, labels = data
        # calculate outputs by running images through the network
        outputs = net(images)
        # the class with the highest energy is what we choose as prediction
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print(f'Accuracy of the network on the {total} test images: {100 * correct // total} %')

# prepare to count predictions for each class
correct_pred = {classname: 0 for classname in class_labels}
total_pred = {classname: 0 for classname in class_labels}
net.eval()
# again no gradients needed
with torch.no_grad():
    for data in test_loader:  # test_loader:
        images, labels = data
        outputs = net(images)
        _, predictions = torch.max(outputs, 1)
        # collect the correct predictions for each class
        for label, prediction in zip(labels, predictions):
            if label == prediction:
                correct_pred[class_labels[label]] += 1
            total_pred[class_labels[label]] += 1

# print accuracy for each class
for classname, correct_count in correct_pred.items():
    accuracy = 100 * float(correct_count) / total_pred[classname]
    print(f'Accuracy for class: {classname:5s} is {accuracy:.1f} %')


### Confusion Matrix
pred_ = []
true_ = []

# iterate over test data
for inputs, labels in test_loader:
    output = net(inputs)  # Feed Network

    output = (torch.max(torch.exp(output), 1)[1]).data.cpu().numpy()
    pred_.extend(output)  # Save Prediction

    labels = labels.data.cpu().numpy()
    true_.extend(labels)  # Save Truth

# Build confusion matrix
cm_matrix = confusion_matrix(true_, pred_)

df_cm = pd.DataFrame(cm_matrix / np.sum(cm_matrix, axis=1)[:, None], index=[i for i in class_labels],
                     columns=[i for i in class_labels])

plt.figure(figsize=(12, 7))
sn.heatmap(df_cm, annot=True)
plt.savefig(os.path.join('outputs', f'conf_mat_{name_}.png'))
