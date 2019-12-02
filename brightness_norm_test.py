#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 13:18:56 2019

@author: tuan
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils

def hisNorm_and_CLAHE(imgpath):
    image = cv2.imread(imgpath)
    image = imutils.resize(image, width=400)    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    eq = cv2.equalizeHist(image)
    
    clahe = cv2.createCLAHE(clipLimit=2.00, tileGridSize=(8,8))
    cl1 = clahe.apply(image)
    
    return image, eq, cl1

imgpath = './board/11.jpg'
image, eq, clahe = hisNorm_and_CLAHE(imgpath)

res = np.hstack((image, eq, clahe))
cv2.imshow('res', res)