'''
    Author: Sungguk Cha
    eMail : navinad@naver.com
    dataloader for word embedding classifier training
'''

import fasttext as ft
import os
import numpy as np
import random
import scipy.misc as m
import torch

from dataloaders.word import get_maps
from PIL import Image
from torch.utils import data
from mypath import Path
from torchvision import transforms

class ToTensor(object):
    """ Convert ndarrays in sample to Tensors. """
    def __call__(self, sample):
        emb = sample['embedding']
        label = sample['label']

        emb = torch.from_numpy(emb).float()

        return {'embedding': emb, 'label': label}

class Embedding(data.Dataset):
    
    def __init__(self, args):
        
        if args.dataset == 'pascal':
            self.NUM_CLASSES = 21
            self.words = get_maps('pascal')

        model_path = os.path.join('../../datasets/wiki.en/', 'wiki.en.bin')
        self.model = ft.load_model(model_path)

        self.positives = []
        for i in range(1, len(words)):
            self.positives.append( self.words[i] )
            
        self.negatives = []
        for i in range(len(self.model.words)):
            if self.model.words[i] in self.positivies: continue
            self.negatives.append(self.model.words[i])
        
        self.class_map = dict(zip(self.valid_classes, range(self.NUM_CLASSES)))

        if len(self.positives) == 0 or len(self.negatives) == 0:
            raise Exception("No word loaded")

        print("Found %d %d words" % (len(self.positives), len(self.negatives)))

    def __len__(self):
        return len(self.negatives*2)

    def __getitem__(self, index):
        # Please make sure to reset random seed every epoch
        # random.seed(index)
        R = random.random()
        if R < 0.5: # positive
            r = random.randint(0, len(self.positives))
            word = self.positives[r]
            embedding = self.model[word]
            label = r + 1
        else: # negative
            r = random.randint(0, len(self.negatives))
            word = self.negatives[r]
            embedding = self.model[word]
            label = 0

        sample = {'embedding': embedding, 'label': label}
        
        composed_transforms = transforms.Compose([
                ToTensor() ])

        return composed_transforms(sample)
