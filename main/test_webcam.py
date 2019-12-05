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

# Replace the URL with your own IPwebcam shot.jpg IP:port
url='http://192.168.0.104:8080/shot.jpg'

while True:

    # Use urllib to get the image and convert into a cv2 usable format
    imgResp=urllib.request.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    img = imutils.resize(img, width=1000)

    # put the image on screen
    cv2.imshow('IPWebcam',img)

    #To give the processor some less stress
    time.sleep(0.5) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break