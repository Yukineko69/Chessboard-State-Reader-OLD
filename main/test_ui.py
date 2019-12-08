#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 00:59:40 2019

@author: tuan
"""

from ChessGUI import Application
import cv2

url = 'http://192.168.1.2:8080/photo.jpg'
app = Application(url)
app.mainloop()