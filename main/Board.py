#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 13:29:32 2019

@author: tuan
"""

import cv2
import numpy as np
import math

debug = False

class Board:
    def __init__(self, squares):
        self.squares = squares
        self.boardMatrix = []
        self.promotion = 'q'
        self.promo = False
        self.move = "e2e4"

    def.draw(self, image):
        for square in self.squares:
            square.draw(image, (0,0,255))
