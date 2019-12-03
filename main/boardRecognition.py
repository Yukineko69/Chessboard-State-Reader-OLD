#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 13:28:36 2019

@author: tuan
"""

import math
import cv2
import numpy as np
import imutils
from Line import Line
from Square import Square
from Board import Board

debug = False

class boardRecognition:
    def __init__(self, camera):
        self.cam = camera

    def initializeBoard(self):
        corners = []
        while len(corners) < 81:
            image = self.cam.takePicture()
            # Threshold image
            adaptiveThresh, img = self.cleanImage(image)
            # Remove background
            mask = self.initializeMask(adaptiveThresh, img)
            # Detect edges
            edges, colorEdges = self.detectEdges(mask)
            # Detect lines
            horizontal, vertical = self.detectLines(edges, colorEdges)
            # Detect corners
            corners = self.detectCorners(horizontal, vertical, colorEdges)

        # Detect squares
        squares = self.detectSquares(corners, img)
        # Create board
        board = Board(squares)

        return board

    def cleanImage(self, image):
        # Resize
        img = imutils.resize(image, width=500)
        # Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
