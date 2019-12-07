#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 13:29:54 2019

@author: tuan
"""

import numpy as np
import cv2

class Square:
    '''
    Squares of chessboard
    '''
    def __init__(self, image, c1, c2, c3, c4, position, state=''):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4

        self.position = position

        # Square contour
        self.contour = np.array([c1, c2, c3, c4], dtype=np.int32)

        # Center of Square
        M = cv2.moments(self.contour)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        # Region of interest
        self.roi = (cx, cy)
        self.radius = 10

        self.emptyColor = self.roiColor(image)
        self.state = state

    def draw(self, image, color, thickness=2):
        ctr = np.array(self.contour).reshape((-1,1,2)).astype(np.int32)
        cv2.drawContours(image, [ctr], 0, color, thickness, cv2.LINE_AA)

    def drawROI(self,image, color, thickness=1):
        cv2.circle(image, self.roi, self.radius, color, thickness, cv2.LINE_AA)

    def roiColor(self, image):
        # Init mask
        maskImage = np.zeros((image.shape[0], image.shape[1]), np.uint8)
        # Draw ROI circle on mask
        cv2.circle(maskImage, self.roi, self.radius, (255,255,255), -1, cv2.LINE_AA)
        # Find average color
        averageColor = cv2.mean(image, mask=maskImage)[::-1]
        averageColor = (int(averageColor[1]), int(averageColor[2]), int(averageColor[3]))

        return averageColor

    def namedTheSquare(self, image):
        cv2.putText(image, self.position, self.roi, cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0,255,0), 1, cv2.LINE_AA)
