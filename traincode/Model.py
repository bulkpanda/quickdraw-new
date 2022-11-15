# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 17:56:24 2021

@author: Kunal Patel
"""
#Building the model
import torch
import torch.nn as nn
from torchvision import models
import torch.nn.functional as F

class Quickdraw_Net(nn.Module):
  def __init__(self):  # Constructor

    super(Quickdraw_Net, self).__init__()

    self.relu = nn.ReLU(inplace=True)

    self.conv1 = nn.Conv2d(1,32,3,padding=1)
    self.bn1 = nn.BatchNorm2d(32)
    self.pool1 = nn.MaxPool2d(2,2,ceil_mode=True) #32x32

    self.conv2 = nn.Conv2d(32,64,3,padding=1)
    self.bn2 = nn.BatchNorm2d(64)
    self.pool2 = nn.MaxPool2d(2,2,ceil_mode=True) #16x16

    self.conv3 = nn.Conv2d(64,128,3,padding=1)
    self.bn3 = nn.BatchNorm2d(128)
    self.pool3 = nn.MaxPool2d(2,2,ceil_mode=True) #8x8

    self.fc1 = nn.Linear(8192,512) #8x8x128
    self.fc2 = nn.Linear(512,128)
    self.fc3 = nn.Linear(128,10)

    self.dropout1 = nn.Dropout(0.25)
    self.dropout2 = nn.Dropout(0.5)

  
  def forward(self,x):
    hx=x
    
    hx1 = self.relu(self.bn1(self.conv1(hx)))
    hx = self.pool1(hx1)
    # print('After conv1: ',hx.shape)

    hx2 = self.relu(self.bn2(self.conv2(hx)))
    hx = self.pool2(hx2)
    # print('After conv2: ',hx.shape)

    hx3 = self.relu(self.bn3(self.conv3(hx)))
    hx = self.pool3(hx3)
    # print('After conv3: ',hx.shape)

    hx=self.dropout1(hx)

    hx=torch.flatten(hx,1)
    # print('After flatten: ',hx.shape)

    hx=self.fc1(hx)
    hx=self.relu(hx)
    # print('After fc1: ',hx.shape)
    hx=self.dropout2(hx)

    hx=self.fc2(hx)
    hx=self.relu(hx)
    # print('After fc2: ',hx.shape)
    hx=self.dropout1(hx)

    hx=self.fc3(hx)
    #print('After fc3: ',hx.dim())
    
    return hx

class Quickdraw_Net2(nn.Module):
  def __init__(self):  # Constructor

    super(Quickdraw_Net2, self).__init__()

    self.relu = nn.ReLU(inplace=True)

    self.conv1 = nn.Conv2d(1,16,3,padding=1)
    self.bn1 = nn.BatchNorm2d(16)
    self.pool1 = nn.MaxPool2d(2,2,ceil_mode=True) #32x32

    self.conv2 = nn.Conv2d(16,32,3,padding=1)
    self.bn2 = nn.BatchNorm2d(32)
    self.pool2 = nn.MaxPool2d(2,2,ceil_mode=True) #16x16


    self.fc1 = nn.Linear(8192,512) #16x16x32
    self.fc2 = nn.Linear(512,128)
    self.fc3 = nn.Linear(128,10)

    self.dropout1 = nn.Dropout(0.25)
    self.dropout2 = nn.Dropout(0.5)

  
  def forward(self,x):
    hx=x
    
    hx1 = self.relu(self.bn1(self.conv1(hx)))
    hx = self.pool1(hx1)
    # print('After conv1: ',hx.shape)

    hx2 = self.relu(self.bn2(self.conv2(hx)))
    hx = self.pool2(hx2)
    # print('After conv2: ',hx.shape)

    hx=self.dropout1(hx)

    hx=torch.flatten(hx,1)
    # print('After flatten: ',hx.shape)

    hx=self.fc1(hx)
    hx=self.relu(hx)
    # print('After fc1: ',hx.shape)
    hx=self.dropout2(hx)

    hx=self.fc2(hx)
    hx=self.relu(hx)
    # print('After fc2: ',hx.shape)
    hx=self.dropout1(hx)

    hx=self.fc3(hx)
    #print('After fc3: ',hx.dim())
    
    return hx