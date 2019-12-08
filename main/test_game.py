#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 02:24:11 2019

@author: tuan
"""

from Game import Game
from ChessGUI import *
import cv2
url = 'http://192.168.1.2:8080/photo.jpg'

game = Game(url)
game.setUp()
game.analyzeBoard()
game.checkBoardIsSet()
cv2.imshow('current',game.current)