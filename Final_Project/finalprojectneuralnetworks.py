from collections import OrderedDict

import torch
import os
from torch import nn
import torch.nn.functional as F
from torch.utils.data import Dataset
from torchvision import datasets, transforms
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class FinalProjectEEGDataset(Dataset):
    """Face Landmarks dataset."""

    def __init__(self, csv_file, root_dir, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the EEG data.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.eeg_data = pd.read_csv(os.path.join(root_dir, csv_file), delimiter=',', usecols=range(15))
        print(self.eeg_data.dtypes)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.eeg_data)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        open_or_closed = self.eeg_data.iloc[idx, 14].astype('float')
        channel_data = self.eeg_data.iloc[idx, 0:14]
        channel_data = np.array([channel_data])
        channel_data = channel_data.astype('float').reshape(-1, 14)
        sample = {'open_or_closed': open_or_closed, 'channel_data': channel_data}

        if self.transform:
            sample = self.transform(sample)

        return channel_data, open_or_closed


class NeuralNetwork(nn.Module):
    def __init__(self, num_inputs, num_hidden_units_by_layers, num_outputs):
        super(NeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()
        od = OrderedDict([])
        if num_hidden_units_by_layers:
            for i in range(len(num_hidden_units_by_layers)):
                if i == 0:
                    print('i == 0')
                    od['Linear0'] = nn.Linear(num_inputs, num_hidden_units_by_layers[0])
                    od['ReLU0'] = nn.ReLU()
                else:
                    od['Linear' + str(i)] = nn.Linear(num_hidden_units_by_layers[i - 1], num_hidden_units_by_layers[i])
                    od['ReLU' + str(i)] = nn.ReLU()
            od['Linear' + str(len(num_hidden_units_by_layers))] = \
                nn.Linear(num_hidden_units_by_layers[len(num_hidden_units_by_layers) - 1], num_outputs)
        else:
            od['Linear0'] = nn.Linear(num_inputs, num_outputs)

        self.linear_relu_stack = nn.Sequential(od)

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


class CNN(nn.Module):
    def __init__(self, num_inputs, num_hiddens_per_conv_layer, num_hiddens_per_fc_layer, num_outputs,
                 patch_size_per_conv_layer, stride_per_conv_layer):
        super(CNN, self).__init__()
        n_conv_layers = len(num_hiddens_per_conv_layer)
        if (
                len(patch_size_per_conv_layer) != n_conv_layers
                or len(stride_per_conv_layer) != n_conv_layers
        ):
            raise Exception(
                "The lengths of num_hiddens_per_conv_layer, patch_size_per_conv_layer, and stride_per_conv_layer must "
                "be equal. "
            )

        self.flatten = nn.Flatten()
        self.odc = OrderedDict([])
        if num_hiddens_per_conv_layer:
            for i in range(len(num_hiddens_per_conv_layer)):
                if i == 0:
                    print('i == 0')
                    self.odc['Conv1d0'] = nn.Conv1d(num_inputs, num_hiddens_per_conv_layer[0],
                                                    kernel_size=patch_size_per_conv_layer[0],
                                                    stride=stride_per_conv_layer[0])
                    # self.odc['ReLU0'] = nn.ReLU()
                else:
                    self.odc['Conv1d' + str(i)] = nn.Conv1d(num_hiddens_per_conv_layer[i - 1],
                                                            num_hiddens_per_conv_layer[i],
                                                            kernel_size=patch_size_per_conv_layer[i],
                                                            stride=stride_per_conv_layer[i])
                    # self.odc['ReLU' + str(i)] = nn.ReLU()

        self.od = OrderedDict([])
        if num_hiddens_per_fc_layer:
            for i in range(len(num_hiddens_per_fc_layer)):
                if i == 0:
                    print('i == 0')
                    self.od['Linear0'] = nn.Linear(num_hiddens_per_conv_layer[len(num_hiddens_per_conv_layer)-1], num_hiddens_per_fc_layer[0])
                    # self.od['ReLU0'] = nn.ReLU()
                else:
                    self.od['Linear' + str(i)] = nn.Linear(num_hiddens_per_fc_layer[i - 1], num_hiddens_per_fc_layer[i])
                    # self.od['ReLU' + str(i)] = nn.ReLU()
            self.od['Linear' + str(len(num_hiddens_per_fc_layer))] = \
                nn.Linear(num_hiddens_per_fc_layer[len(num_hiddens_per_fc_layer) - 1], num_outputs)
        else:
            self.od['Linear0'] = nn.Linear(num_inputs, num_outputs)

        # self.conv1d_linear_relu_stack = nn.Sequential(od)

    def forward(self, x):
        x = x.unsqueeze(dim=0)
        for conv_layer in self.odc:
            print(self.odc[conv_layer])
            x = F.relu(self.odc[conv_layer](x))

        # x = torch.flatten(x, 1)  # flatten all dimensions except batch
        x = x.squeeze()
        for i, layer in enumerate(self.od):
            if i == len(self.od) - 1:
                x = self.od[layer](x)
            else:
                x = F.relu(self.od[layer](x))

        return x
