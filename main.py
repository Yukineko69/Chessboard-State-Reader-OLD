#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 22:28:26 2019

@author: tuan
"""

import cv2
import numpy as np
import imutils
import math


def removeBackground(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th3 = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                                cv2.THRESH_BINARY,125,1)
    contours, hierarchy = cv2.findContours(th3,
                                       cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)
    imgContours = img.copy()    
    for c in range(len(contours)):
        area = cv2.contourArea(contours[c])
        perimeter = cv2.arcLength(contours[c], True)
        if c == 0:
            Lratio = 0
        if perimeter > 0:
            ratio = area / perimeter
            if ratio > Lratio:
                largest=contours[c]
                Lratio = ratio
#                Lperimeter=perimeter
#                Larea = area
        else:
            pass
    cv2.drawContours(imgContours, [largest], -1, (0,255,0), 2)
    chessboardEdge = cv2.approxPolyDP(largest, 0, True)
    mask = np.zeros_like(img_gray)
    cv2.fillConvexPoly(mask, chessboardEdge, 255, 1)
    extracted = np.zeros_like(img)
    extracted[mask == 255] = img[mask == 255]
    
    return extracted

def getChessboardEdges(img):
    canny = cv2.Canny(img, 10, 250)    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, kernel, iterations=1)
    closed = cv2.dilate(closed, kernel, iterations=1)
#    cv2.imshow('closed', closed)
    
    cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key = cv2.contourArea, reverse = True)[1]
    peri = cv2.arcLength(c, True)
    edgeApprox = cv2.approxPolyDP(c, 0.1 * peri, True)
    
    imgContours = img.copy()
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.drawContours(imgContours, [edgeApprox], -1, (0,255,0), 2)
    mask = np.zeros_like(img_gray)
    cv2.fillConvexPoly(mask, edgeApprox, 255, 1)
    extracted = np.zeros_like(img)
    extracted[mask == 255] = img[mask == 255]
    
    return extracted, edgeApprox

def checkLineOrientation(line):
    [[x1, y1, x2, y2]] = line
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) > abs(dy):
        return "horizontal"
    else:
        return "vertical"

def lineSegmentation(img):
    blur = cv2.medianBlur(img, 3)
    canny = cv2.Canny(blur, 50, 250)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    canny = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)
    canny = cv2.dilate(canny, None, iterations=1)
    
    lines = cv2.HoughLinesP(canny, 1, np.pi/180, 150, minLineLength=200, maxLineGap=10)
    for line in lines:
        x1,y1,x2,y2 = line[0]
        cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 2)
        
    horizontal = []
    vertical = []
    for line in lines:
        if checkLineOrientation(line) == 'horizontal':
            horizontal.append(line)
        else:
            vertical.append(line)
    
    return img, horizontal, vertical
    
def findIntersect(h, v):
    [[x1, y1, x2, y2]] = h
    [[X1, Y1, X2, Y2]] = v
    
    x = ((x1*y2 - x2*y1) * (X1-X2) - (x1 - x2) * (X1*Y2 - X2*Y1)) / \
        ((x1 - x2) * (Y1 - Y2) - (y1 - y2) * (X1 - X2))
    y = ((x1*y2 - x2*y1) * (Y1-Y2) - (y1 - y2) * (X1*Y2 - X2*Y1)) / \
        ((x1 - x2) * (Y1 - Y2) - (y1 - y2) * (X1 - X2))
    x = int(x)
    y = int(y)
    return [x,y]

def detectCorners(img, vertical, horizontal):
    corners = []
    for v in vertical:
        for h in horizontal:
            corner = findIntersect(h, v)
            corners.append(corner)
    
    dedupeCorners = []
    for c in corners:
        matchingFlag = False
        for d in dedupeCorners:
            if math.sqrt((d[0]-c[0])*(d[0]-c[0]) + (d[1]-c[1])*(d[1]-c[1])) < 10:
                matchingFlag = True
                break
        if not matchingFlag:
            dedupeCorners.append(c)
    
    for c in dedupeCorners:
        cv2.circle(img, (c[0], c[1]), 10, (0,0,255))
        
    return img, dedupeCorners

imgpath = './board/11.jpg'
img = cv2.imread(imgpath)
img = imutils.resize(img, width=500)
cv2.imshow('img', img)

extracted = removeBackground(img)
cv2.imshow('ex', extracted)    

ex2, edges = getChessboardEdges(extracted)

ex2, horizontal, vertical = lineSegmentation(ex2)

cv2.imshow('ex2', ex2)

ex2, corners = detectCorners(ex2, vertical, horizontal)
    
cv2.imshow('ex2', ex2)

corners.sort(key=lambda x: x[0])
rows = [[],[],[],[],[],[],[],[],[]]
r = 0
for c in range(0, 81):
    if c > 0 and c % 9 == 0:
        r = r + 1
    rows[r].append(corners[c])
    
letters = ['a','b','c','d','e','f','g','h']
numbers = ['1','2','3','4','5','6','7','8']
Squares = []

for r in rows:
    r.sort(key=lambda y: y[1])

for r in range(8):
    for c in range(8):
        c1 = rows[r][c]
        c2 = rows[r][c+1]
        c3 = rows[r+1][c]
        c4 = rows[r+1][c+1]
        
        position = letters[r] + numbers[7-c]
        #draw
        contour = np.array([c1,c2,c4,c3], dtype=np.int32)
        ctr = np.array(contour).reshape((-1,1,2)).astype(np.int32)
        cv2.drawContours(ex2, [ctr], 0, (0,255,0), 2)
        #drawROI
        M = cv2.moments(contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        roi = (cx, cy)
        radius = 7
        cv2.circle(ex2, roi, radius, (255,0,0), 3)

cv2.imshow('ex2', ex2)
