# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 17:57:26 2021

@author: Kunal Patel
"""
import os
import torch
import torch.nn as nn
import torch.optim as optim
import Model
from dataloader import data_loader
import config as cg
import matplotlib.pyplot as plt
import numpy as np

#=============================Train Model======================================
train_loss_array=[]
def train(model, use_cuda, train_loader, optimizer, epoch):

    model.train()  # Tell the model to prepare for training
    
    for batch_idx, (data, target) in enumerate(train_loader):  # Get the batch

        if use_cuda:
            data, target = data.cuda(), target.cuda() # Sending the data to GPU
        
        optimizer.zero_grad()  # Setting the cumulative gradients to 0
        output = model(data)  # Forward pass through the model
        loss = nn.functional.cross_entropy(output, target)
        train_loss_array.append(loss)
        loss.backward()  # Calculating the gradients of the model.
        optimizer.step()  # Updating the model parameters.

        if (batch_idx+1)%100==0:
            print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
            epoch, batch_idx * len(data), len(train_loader.dataset),
            100. * batch_idx / len(train_loader), loss.item()))    
#==============================================================================

#==============================Test Model======================================
test_loss_array=[]
accuracy=[]
def test(model, use_cuda, test_loader):

  model.eval()  # Tell the model to prepare for testing or evaluation

  test_loss = 0
  correct = 0
  with torch.no_grad():  # Tell the model that gradients need not be calculated
        
    for batch_idx, (data, target) in enumerate(test_loader):  # Get the batch

      if use_cuda:
        data, target = data.cuda(), target.cuda()

      output = model(data)  # Forward pass
      # sum up batch loss
      test_loss += torch.sum(nn.functional.cross_entropy(output, target)) 
      # get the index of the maximum output
      pred = output.argmax(dim=1, keepdim=True)  
      # Get total number of correct samples
      correct += pred.eq(target.view_as(pred)).sum().item()  
  accuracy.append(100. * correct / len(test_loader.dataset))
  test_loss /= len(test_loader.dataset) #Accuracy = Total Correct/Total Samples
  test_loss_array.append(test_loss)
  print('\nTest set: Average loss: {:.4f}, Accuracy: {}/{} ({:.0f}%)\n'.format(
        test_loss, correct, len(test_loader.dataset),
        100. * correct / len(test_loader.dataset)))  
#============================================================================== 
  
#Calling the model 
model=Model.Quickdraw_Net2()
use_cuda=False

if torch.cuda.is_available():
    model.cuda()
    use_cuda=True

#============================Loading data======================================    
print('Starting Dataloader')
train_loader = data_loader.getdataloader('train',True)
test_loader = data_loader.getdataloader('test',True)
print('Data loaded')
#==============================================================================

#Setting the optimizer
optimizer = optim.Adam(model.parameters(), lr=cg.lr, betas=(0.9, 0.999), 
                       eps=1e-08, weight_decay=0)

#=========================Start the training===================================
for epoch in range(1, cg.iterations['train']+1):
  train(model, use_cuda, train_loader, optimizer, epoch )
  
  #checking model every 10 epochs
  if epoch % 10 == 0:
    test(model, use_cuda, test_loader )
    if torch.cuda.is_available():
        dummy_input=torch.randn(1,1,64,64).cuda()
    else:
        dummy_input=torch.randn(1,1,64,64)
    savepath=cg.savepath
    os.makedirs(savepath, exist_ok=True)
    
    #saving model every 10 epochs
    torch.onnx.export(model, dummy_input, savepath+ '/'+str(epoch) 
    +'model.onnx',verbose=True, input_names=['data'], output_names=['output'])
    
    plt.title(' Train Loss'+str(epoch))
    plt.plot([j for j in range(len(train_loss_array))], train_loss_array)
    plt.show() 
    #plt.savefig('Train loss'+str(epoch))

    plt.title(' Test Loss'+str(epoch))
    plt.plot([j for j in range(len(test_loss_array))], test_loss_array)
    plt.show()    
    #plt.savefig('Test loss'+str(epoch))

    plt.title(' Accuracy'+str(epoch))
    plt.plot([j for j in range(len(accuracy))], accuracy)
    plt.show() 
    #plt.savefig('Accuracy'+str(epoch))
#==============================================================================


#saving error data
np.save('train_loss.npy', train_loss_array)
np.save('test_loss.npy', test_loss_array)
np.save('accuracy.npy', accuracy)

#===================Plotting error curves======================================
plt.title(' Train Loss')
plt.plot([j for j in range(len(train_loss_array))], train_loss_array)
plt.savefig('Train loss')
plt.show() 


plt.title(' Test Loss')
plt.plot([j for j in range(len(test_loss_array))], test_loss_array)
plt.savefig('Test loss')
plt.show()    


plt.title(' Accuracy')
plt.plot([j for j in range(len(accuracy))], accuracy)
plt.savefig('Accuracy')
plt.show() 

#==============================================================================

#Saving the final model
if torch.cuda.is_available():
  dummy_input=torch.randn(1,1,64,64).cuda()
else:
  dummy_input=torch.randn(1,1,64,64)
savepath=cg.savepath
os.makedirs(savepath, exist_ok=True)
torch.onnx.export(model, dummy_input, savepath+'/model.onnx',verbose=True,
                  input_names=['data'], output_names=['output'])  