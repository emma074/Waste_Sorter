# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Xn_-kw7zudEb28n1cbayIhZNq8OumCbo
"""

import fastai

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %reload_ext autoreload
# %autoreload 2
# %matplotlib inline

# %config InlineBackend.figure_format = 'retina'

from fastai.vision import *
from fastai.metrics import error_rate

from pathlib import Path
from glob2 import glob
from sklearn.metrics import confusion_matrix
import random
import pandas as pd
import numpy as np
import os
import zipfile as zf
import shutil
import re
import seaborn as sns

#from zipfile import ZipFile
#with ZipFile("/content/drive/MyDrive/Waste_dataset/dataset-resized.zip",'r') as zipObj:
 # zipObj.extractall("/content/drive/MyDrive")

os.listdir(os.path.join(os.getcwd(),"/content/drive/MyDrive/dataset-resized/dataset-resized"))

os.getcwd()

waste_type = 'cardboard'
source_folder = os.path.join('', waste_type)

# Check if the folder exists and create it if it doesn't
if not os.path.exists(source_folder):
    os.makedirs(source_folder)

waste_type = 'paper'
source_folder = os.path.join('', waste_type)

# Check if the folder exists and create it if it doesn't
if not os.path.exists(source_folder):
    os.makedirs(source_folder)

waste_type = 'glass'
source_folder = os.path.join('', waste_type)

# Check if the folder exists and create it if it doesn't
if not os.path.exists(source_folder):
    os.makedirs(source_folder)

waste_type = 'plastic'
source_folder = os.path.join('', waste_type)

# Check if the folder exists and create it if it doesn't
if not os.path.exists(source_folder):
    os.makedirs(source_folder)

waste_type = 'trash'
source_folder = os.path.join('', waste_type)

# Check if the folder exists and create it if it doesn't
if not os.path.exists(source_folder):
    os.makedirs(source_folder)

waste_type = 'metal'
source_folder = os.path.join('', waste_type)

# Check if the folder exists and create it if it doesn't
if not os.path.exists(source_folder):
    os.makedirs(source_folder)

def split_indices(folder,seed1,seed2):
    n = len(os.listdir(folder))
    full_set = list(range(1,n+1))

    ## train indices
    random.seed(seed1)
    train = random.sample(list(range(1,n+1)),int(.5*n))

    ## temp
    remain = list(set(full_set)-set(train))

    ## separate remaining into validation and test
    random.seed(seed2)
    valid = random.sample(remain,int(.5*len(remain)))
    test = list(set(remain)-set(valid))

    return(train,valid,test)

## gets file names for a particular type of trash, given indices
    ## input: waste category and indices
    ## output: file names
def get_names(waste_type,indices):
    file_names = [waste_type+str(i)+".jpg" for i in indices]
    return(file_names)
## moves group of source files to another folder
    ## input: list of source files and destination folder
    ## no output
def move_files(source_files,destination_folder):
    for file in source_files:
        shutil.move(file,destination_folder)

import os
import random

def split_indices(source_folder, train_ratio, valid_ratio):
    all_files = os.listdir(source_folder)
    num_files = len(all_files)
    indices = list(range(num_files))
    random.shuffle(indices)

    train_size = int(num_files * train_ratio)
    valid_size = int(num_files * valid_ratio)

    train_indices = indices[:train_size]
    valid_indices = indices[train_size:(train_size + valid_size)]
    test_indices = indices[(train_size + valid_size):]

    return train_indices, valid_indices, test_indices

def get_names(waste_type, indices):
    # Assuming that the filenames follow a specific pattern
    # For example: "waste_type_1.jpg", "waste_type_2.jpg", ...
    return [f"{waste_type}_{index}.jpg" for index in indices]

import shutil

def move_files(source_files, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for source_file in source_files:
        shutil.move(source_file, destination_folder)

## paths will be train/cardboard, train/glass, etc...
subsets = ['train','valid']
waste_types = ['cardboard','glass','metal','paper','plastic','trash']

## create destination folders for data subset and waste type
for subset in subsets:
    for waste_type in waste_types:
        folder = os.path.join('data',subset,waste_type)
        if not os.path.exists(folder):
            os.makedirs(folder)
if not os.path.exists(os.path.join('data','test')):
    os.makedirs(os.path.join('data','test'))

## move files to destination folders for each waste type
for waste_type in waste_types:
    source_folder = os.path.join('',waste_type)
    train_ind, valid_ind, test_ind = split_indices(source_folder,1,1)

    ## move source files to train
    train_names = get_names(waste_type,train_ind)
    train_source_files = [os.path.join(source_folder,name) for name in train_names]
    train_dest = "data/train/"+waste_type
    move_files(train_source_files,train_dest)

    ## move source files to valid
    valid_names = get_names(waste_type,valid_ind)
    valid_source_files = [os.path.join(source_folder,name) for name in valid_names]
    valid_dest = "data/valid/"+waste_type
    move_files(valid_source_files,valid_dest)

    ## move source files to test
    test_names = get_names(waste_type,test_ind)
    test_source_files = [os.path.join(source_folder,name) for name in test_names]
    ## I use data/test here because the images can be mixed up
    move_files(test_source_files,"data/test")

from fastai.vision import *

from fastai.vision.all import *
from fastai.vision.data import *

# Define your data block
data_block = DataBlock(
    blocks=(ImageBlock, CategoryBlock),  # Modify as needed for your dataset
    get_items=get_image_files,  # Function to get image file paths
    splitter=RandomSplitter(valid_pct=0.2, seed=42),  # Split dataset into train and validation
    get_y=parent_label,  # Modify this to suit your dataset's label structure
    item_tfms=Resize(460),  # Resize images to a uniform size
    batch_tfms=[*aug_transforms(size=224), Normalize.from_stats(*imagenet_stats)]  # Data augmentation and normalization
)

# Define your data loaders
data = data_block.dataloaders("/content/drive/MyDrive/dataset-resized/dataset-resized", bs=16)

# View the data batch
data.show_batch()

data

data.show_batch(figsize=(10,8))

from fastai.vision.all import *
import matplotlib.pyplot as plt

# Define DataLoaders (data) as shown previously
# ...

# Create a Learner
learn = vision_learner(data, resnet34, metrics=accuracy)

# Train your model and specify the recorder
learn.fine_tune(25, cbs=ShowGraphCallback())

plt.show()

interp = ClassificationInterpretation.from_learner(learn)
losses,idxs = interp.top_losses()

interp.plot_top_losses(9, figsize=(15,11))

doc(interp.plot_top_losses)
interp.plot_confusion_matrix(figsize=(12,12), dpi=60)

interp.most_confused(min_val=2)

# Validate the model on the validation dataset
result = learn.validate()

# Extract the accuracy from the validation result
accuracy = result[1]  # Index 1 corresponds to accuracy in the result tuple

# Print the accuracy
print(f'Validation Accuracy: {accuracy * 100:.2f}%')

from fastai.vision.all import *
import matplotlib.pyplot as plt

# Define DataLoaders (data) as shown previously
# ...

# Create a Learner with ResNet50
learn = vision_learner(data, resnet50, metrics=accuracy)

# Train your model and specify the recorder
learn.fine_tune(10, cbs=ShowGraphCallback())

plt.show()

interp = ClassificationInterpretation.from_learner(learn)
losses,idxs = interp.top_losses()

interp.plot_top_losses(9, figsize=(15,11))

doc(interp.plot_top_losses)
interp.plot_confusion_matrix(figsize=(12,12), dpi=60)

# Validate the model on the validation dataset
result = learn.validate()

# Extract the accuracy from the validation result
accuracy = result[1]  # Index 1 corresponds to accuracy in the result tuple

# Print the accuracy
print(f'Validation Accuracy: {accuracy * 100:.2f}%')

from fastai.vision.all import *
import matplotlib.pyplot as plt

# Define DataLoaders (data) as shown previously
# ...

# Create a Learner with DenseNet121
learn = vision_learner(data, densenet121, metrics=accuracy)

# Train your model and specify the recorder
learn.fine_tune(10, cbs=ShowGraphCallback())

plt.show()

interp.plot_top_losses(9, figsize=(15,11))

doc(interp.plot_top_losses)
interp.plot_confusion_matrix(figsize=(12,12), dpi=60)

# Validate the model on the validation dataset
result = learn.validate()

# Extract the accuracy from the validation result
accuracy = result[1]  # Index 1 corresponds to accuracy in the result tuple

# Print the accuracy
print(f'Validation Accuracy: {accuracy * 100:.2f}%')