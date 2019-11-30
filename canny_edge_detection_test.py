#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 01:33:30 2019

@author: tuan
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils

img = cv2.imread('./temp/false-0.jpg',0)
img = imutils.resize(img, width=400)
img = cv2.medianBlur(img, 5)
ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
edges = cv2.Canny(th1,200,200)

contours, hierarchy = cv2.findContours(th1,
                                       cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)
imgContours = img.copy()

for c in range(len(contours)):
    # Area
    area = cv2.contourArea(contours[c])
    # Perimenter
    perimeter = cv2.arcLength(contours[c], True)
    # Filtering the chessboard edge / Error handling as some contours are so small so as to give zero division
    #For test values are 70-40, for Board values are 80 - 75 - will need to recalibrate if change
    #the largest square is always the largest ratio
    if c ==0:
        Lratio = 0
    if perimeter > 0:
        ratio = area / perimeter
        if ratio > Lratio:
            largest=contours[c]
            Lratio = ratio
            Lperimeter=perimeter
            Larea = area
    else:
        pass
# Draw contours
cv2.drawContours(imgContours, [largest], -1, (0,255,0), 3)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()