# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 11:58:54 2021

@author: Kunal Patel
"""

from torch.utils.data import Dataset, DataLoader
import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from torchvision import datasets, transforms
import config as cg

basepath=cg.basepath
lr=cg.lr
savepath=cg.savepath
seed=cg.seed
batchsize=cg.batchsize
iterations=cg.iterations
datasize=cg.datasize
num_workers=cg.num_workers

# =============================================================================
# # Save
# dictionary = {'hello':'world'}
# np.save('my_file.npy', dictionary) 
# 
# # Load
# read_dictionary = np.load('my_file.npy',allow_pickle='TRUE').item()
# print(read_dictionary['hello']) # displays "world"
# =============================================================================
class data_loader(Dataset):
  def __init__(self,type_,isdatafile):
    self.type_=type_
    self.allclasses=sorted(os.listdir(basepath+'/'+type_))
    if isdatafile:
        print('File already present, starting to load data')
        self.alldata=np.load('all_data'+type_+'.npy',allow_pickle='TRUE').item()
        print('data loaded from file')
    else:
        for classI in self.allclasses:
            self.alldata[classI]=[]
            imagepath=sorted(os.listdir(basepath+'/'+type_+'/'+classI+'/image'))
        for image in imagepath:
            print(classI, image)
            image=self.process(basepath+'/'+type_+'/'+classI+'/image/'+image)
            self.alldata[classI].append(image) #alldata contains the image data
            
        np.save('all_data'+type_+'.npy', self.alldata)     
    self.transforms = transforms.Compose([transforms.ToTensor()])     
    
  def process(self,path):
    image=Image.fromarray(plt.imread(path)[:,:,3])
    image=np.array(image.resize((64,64)))
    image=(np.array(image)>0.1).astype(np.float32)[None,:,:] #get image of shape(1,64,64)
    return image

  def __getitem__(self, item):
    classid=np.random.randint(len(self.alldata))
    classname=self.allclasses[classid]
    image_id=np.random.randint(len(self.alldata[classname]))
    image = self.alldata[classname][image_id]
    image=self.transforms(image).permute(1,2,0)    #get image of shape(1,128,128)
    return image, classid

  def _worker_init_fn(worker_id):
    np.random.seed(worker_id)

  def __len__(self):
    return datasize[self.type_]

  def getdataloader(type_='train',isdatafile=False):
    return DataLoader(
        data_loader(type_,isdatafile),
        batch_size=batchsize[type_],
        num_workers=num_workers[type_],
        worker_init_fn=data_loader._worker_init_fn
        )

#Testing the dataloader

# =============================================================================
# train_loader = data_loader.getdataloader('train')
# test_loader = data_loader.getdataloader('test')
# for no, (images, labels) in enumerate(train_loader):
#   print(images[0][0,:,:].shape)
#   plt.imshow(images[1][0,:,:])
#   print(labels)
# =============================================================================
