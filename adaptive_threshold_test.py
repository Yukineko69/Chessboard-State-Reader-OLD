#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 22:28:26 2019

@author: tuan
"""

import cv2
import numpy as np
import imutils


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
    cv2.imshow('closed', closed)
    
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
    
    blur = cv2.medianBlur(extracted, 3)
    canny = cv2.Canny(blur, 50, 250)
    
    return canny, extracted, edgeApprox
    

imgpath = './board/11.jpg'
img = cv2.imread(imgpath)
img = imutils.resize(img, width=400)

extracted = removeBackground(img)
cv2.imshow('ex', extracted)

canny, ex2, edges = getChessboardEdges(extracted)
cv2.imshow('canny', canny)
cv2.imshow('ex2', ex2)


