#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 01:53:00 2019

@author: tuan
"""

import urllib
import cv2
import numpy as np
import time
import imutils

class Camera:
    def __init__(self, url):
        self.url = url

    def takePicture(self):
        imgResponse = urllib.request.urlopen(self.url)
        imgNp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)
        img = imutils.resize(img, width=500)
        time.sleep(0.5)

        return img
