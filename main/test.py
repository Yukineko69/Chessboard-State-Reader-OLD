#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 00:55:08 2019

@author: tuan
"""

import numpy as np
import cv2
import imutils
from boardRecognition import boardRecognition
from Board import Board

imgpath = '../board/13.jpg'
img = cv2.imread(imgpath)
img = imutils.resize(img, width=500)
cv2.imshow('img', img)

br = boardRecognition(img)
thresh, img = br.cleanImage(img)
extracted = br.initializeMask(thresh, img)
edges, colorEdges = br.detectEdges(extracted)
horizontal, vertical = br.detectLines(edges, colorEdges)
corners = br.detectCorners(horizontal, vertical, colorEdges)
squares = br.detectSquares(corners, colorEdges)

board = Board(squares)
board.draw(img)
cv2.imshow('img2',img)
board.assignState()