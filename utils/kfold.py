# -*- coding: utf-8 -*-
"""
Created on Wed May 13 19:48:48 2020

@author: Manuel Pinar-Molina
"""
import os
import numpy as np
from natsort import natsorted
import re
import sys
from sklearn.model_selection import KFold

path_train = 'C:/Users/manue/Desktop/Universidad/DOCTORADO/TEORIA/Point_Cloud/pointnet-tuberias/data/data_h5/full'
n_splits = 5
kf = KFold(n_splits)


total_data = []
pass_count = 0
for folder in sorted(os.listdir(path_train)):
      if re.search("\.(h5)$", folder):  # if the file is a h5
          train_list = open(os.path.join(path_train, 'train_list.txt'), 'w')
          for i in range(19):
              h5_filename = os.path.join('data_' + str(i) + '.h5')
              train_list.write(os.path.basename(h5_filename)+'\n')
              if pass_count == 0:
                  total_data.append(h5_filename)  

      pass_count = 1

index = 0
for train_index, valid_index in kf.split(total_data):
    train_list_j = open(os.path.join(path_train, 'train_list_'+ str(index) + '.txt'), 'w')
    for i in range(len(train_index)):
        h5_filename = os.path.join('data_' + str(train_index[i]) + '.h5')
        train_list_j.write(os.path.basename(h5_filename)+'\n')
    
    valid_list_j = open(os.path.join(path_train, 'valid_list_'+ str(index) + '.txt'), 'w')
    for j in range(len(valid_index)):
        h5_filename = os.path.join('data_' + str(valid_index[j]) + '.h5')
        valid_list_j.write(os.path.basename(h5_filename)+'\n')
            
    index += 1            
    print(train_index, valid_index)


