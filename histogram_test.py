#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 11:31:09 2019

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
    
    return eq, cl1


img = cv2.imread('./board/11.jpg', 0)

hist, bins = np.histogram(img.flatten(), 256, [0, 256])

cdf = hist.cumsum()
cdf_normalized = cdf * hist.max()/cdf.max()


equ = cv2.equalizeHist(img)


clahe = cv2.createCLAHE(clipLimit=2.00, tileGridSize=(8, 8))
cl1 = clahe.apply(img)

hist3, bins3 = np.histogram(cl1.flatten(), 256, [0, 256])
cdf3 = hist3.cumsum()
cdf_normalized3 = cdf3 * hist3.max()/cdf3.max()

res = np.hstack((img, equ, cl1))
cv2.imshow('res', res)


cdf_m = np.ma.masked_equal(cdf, 0)
cdf_m = (cdf_m - cdf_m.min()) * 255/(cdf_m.max() - cdf_m.min())
cdf = np.ma.filled(cdf_m, 0).astype('uint8')

img2 = cdf[img]

hist2, bins2 = np.histogram(img2.flatten(), 256, [0, 256])
cdf2 = hist2.cumsum()
cdf_normalized2 = cdf2 * hist2.max()/cdf2.max()


#plt.plot(cdf_normalized, color='b')
#plt.hist(img.flatten(), 256, [0, 256], color='r')
#plt.xlim([0, 256])
#plt.legend(('cdf', 'histogram'), loc='upper left')
#plt.show()

#plt.figure()
#plt.plot(cdf_normalized2, color='b')
#plt.hist(img2.flatten(), 256, [0, 256], color='r')
#plt.xlim([0, 256])
#plt.legend(('cdf2', 'histogram2'), loc='upper left')
#plt.show()
#
#
#plt.figure()
#plt.plot(cdf_normalized3, color='b')
#plt.hist(img3.flatten(), 256, [0, 256], color='r')
#plt.xlim([0, 256])
#plt.legend(('cdf3', 'histogram3'), loc='upper left')
#plt.show()

fig, ax = plt.subplots(1, 3)
ax[0].plot(cdf_normalized, color='b')
ax[0].hist(img.flatten(), 256, [0, 256], color='r')
fig.legend(('cdf', 'histogram'), loc='upper left')
ax[1].plot(cdf_normalized2, color='b')
ax[1].hist(img2.flatten(), 256, [0, 256], color='r')
ax[2].plot(cdf_normalized3, color='b')
ax[2].hist(cl1.flatten(), 256, [0, 256], color='r')