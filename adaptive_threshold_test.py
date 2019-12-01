#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 22:28:26 2019

@author: tuan
"""

import cv2
import numpy as np
import imutils

img = cv2.imread('./board/11.jpg')
img = imutils.resize(img, width=500)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#cv2.imshow('img', img)

#img_gray = cv2.medianBlur(img_gray, 3)
#cv2.imshow('median blur', img_gray)

ret,th1 = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)
#th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
#            cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
             cv2.THRESH_BINARY,125,1)
#titles = ['Original Image', 'Global Thresholding (v = 127)',
#            'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
#images = [img, th1, th2, th3]
#for i in range(4):
#    plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
#    plt.title(titles[i])
#    plt.xticks([]),plt.yticks([])
#plt.show()

#th3 = cv2.erode(th3, None, iterations=1)
#th3 = inverte(th3)
cv2.imshow('th3', th3)

contours, hierarchy = cv2.findContours(th3,
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
    if c == 0:
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
    
# =============================================================================
# # Draw contour
# cv2.drawContours(imgContours, [largest], -1, (0,255,0), 2)
# cv2.imshow('ct', imgContours)
# # Epsilon parameter needed to fit contour to polygon
# epsilon = 0.1 * Lperimeter
# epsilon = 0
# # Approximates a polygon from chessboard edge
# chessboardEdge = cv2.approxPolyDP(largest, epsilon, True)
# 
# # Create new all black image
# mask = np.zeros_like(img_gray)
# # Copy the chessboard edges as a filled white polygon size of chessboard edge
# cv2.fillConvexPoly(mask, chessboardEdge, 255, 1)
# # Assign all pixels that are white (i.e the polygon, i.e. the chessboard)
# extracted = np.zeros_like(img)
# extracted[mask == 255] = img[mask == 255]
# 
# cv2.imshow('ct', imgContours)
# cv2.imshow('ex', extracted)
# =============================================================================
        
# Draw contour
cv2.drawContours(imgContours, [largest], -1, (0,255,0), 2)
cv2.imshow('ct', imgContours)
# Approximates a polygon from chessboard edge
chessboardEdge = cv2.approxPolyDP(largest, 0, True)
# Create new all black image
mask = np.zeros_like(img_gray)
# Copy the chessboard edges as a filled white polygon size of chessboard edge
cv2.fillConvexPoly(mask, chessboardEdge, 255, 1)
# Assign all pixels that are white (i.e the polygon, i.e. the chessboard)
extracted = np.zeros_like(img)
extracted[mask == 255] = img[mask == 255]

cv2.imshow('ct', imgContours)
cv2.imshow('ex', extracted)



# =============================================================================
# edged = cv2.Canny(extracted, 10, 250)
# cv2.imshow('Canny', edged)
# 
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
# closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
# closed = cv2.erode(closed, None, iterations=2)
# closed = cv2.dilate(closed, None, iterations=1)
# cv2.imshow("Closed", closed)
# 
# cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
# peri = cv2.arcLength(c, True)
# approx = cv2.approxPolyDP(c, 0.01 * peri, True)
# cv2.drawContours(extracted, [approx], -1, (0, 255, 0), 2)
# cv2.imshow('ex', extracted)
# =============================================================================

