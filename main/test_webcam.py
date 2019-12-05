#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 21:30:41 2019

@author: tuan
"""

import urllib
import cv2
import numpy as np
import time
import imutils
from Camera import Camera

url = 'http://192.168.1.4:8080/shot.jpg'

cam = Camera(url)
img = cam.takePicture()
cv2.imshow('img',img)