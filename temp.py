#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 14:05:39 2019

@author: tuan
"""

import cv2
import imutils
#reading the image 
#image = cv2.imread("example.jpg")
image = cv2.imread('./board/11.jpg')
image = imutils.resize(image, width=400)
edged = cv2.Canny(image, 10, 250)
cv2.imshow("Edges", edged)
 
#applying closing function 
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
closed = cv2.erode(closed, None, iterations=1)
cv2.imshow("Closed", closed)
 
#finding_contours 
(cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
for c in cnts:
	peri = cv2.arcLength(c, True)
	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
cv2.imshow("Output", image)