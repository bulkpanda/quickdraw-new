# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 17:51:19 2021

@author: Kunal Patel
"""
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
basepath='./data'
lr=1e-03
savepath='./saved_models/google_data3'
os.makedirs(savepath, exist_ok=True)

seed=0



batchsize={""
    'train':50,
    'test':10
}

iterations={
    'train':100,
    'test':10
}

datasize={
    'train':100000,
    'test':10000
}
num_workers={
    'train':0,
    'test':0
}
