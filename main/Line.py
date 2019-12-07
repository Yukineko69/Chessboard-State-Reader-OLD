#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 13:29:47 2019

@author: tuan
"""

import numpy as np

class Line:
    '''
    Lines of chessboard
    '''
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        self.dx = self.x2 - self.x1
        self.dy = self.y2 - self.y1

        # Orientation
        if abs(self.dx) > abs(self.dy):
            self.orientation = 'horizontal'
        else:
            self.orientation = 'vertical'

    def findIntersection(self, other):
        # Find intersections using linear algebra
        x = ((self.x1*self.y2 - self.y1*self.x2)*(other.x1-other.x2) - (self.x1-self.x2)*(other.x1*other.y2 - other.y1*other.x2))/ ((self.x1-self.x2)*(other.y1-other.y2) - (self.y1-self.y2)*(other.x1-other.x2))
        y = ((self.x1*self.y2 - self.y1*self.x2)*(other.y1-other.y2) - (self.y1-self.y2)*(other.x1*other.y2 - other.y1*other.x2))/ ((self.x1-self.x2)*(other.y1-other.y2) - (self.y1-self.y2)*(other.x1-other.x2))
        x = int(x)
        y = int(y)

        return x, y
