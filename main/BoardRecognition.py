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

class BoardRecognition:
    '''
    Handles the initialization of the board
    Analyzes board to create objects from chessboard
    '''
    def __init__(self, camera):
        self.cam = camera

    def initializeBoard(self):
        corners = []
        while len(corners) < 81:
            image = self.cam.takePicture()
            # TESTING
            # imgpath = '../board/28.jpg'
            # image = cv2.imread(imgpath)
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

        board.draw(image)
        cv2.imwrite('./ProcessImage/InitializedBoard.jpg', image)

        return board

    def cleanImage(self, image):
        # Resize
        img = imutils.resize(image, width=800)
        # Grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Threshold
        adaptiveThresh = cv2.adaptiveThreshold(gray, 255,
                                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                               cv2.THRESH_BINARY, 125, 1)
        if debug:
            cv2.imshow('Adaptive Thresholding', adaptiveThresh)

        return adaptiveThresh, img

    def initializeMask(self, adaptiveThresh, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(adaptiveThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        imgContours = img.copy()

        # Find largest shaped contour
        for c in range(len(contours)):
            area = cv2.contourArea(contours[c])
            perimeter = cv2.arcLength(contours[c], True)

            if c == 0:
                Lratio = 0
            if perimeter > 0:
                ratio = area/perimeter
                if ratio > Lratio:
                    largest = contours[c]
                    Lratio = ratio
                    # Lperimeter = perimeter
                    # Larea = area
                else:
                    pass

        # Draw contours
        cv2.drawContours(imgContours, [largest], -1, (0,255,0), 2, cv2.LINE_AA)
        if debug:
            cv2.imshow('Chess Boarder', imgContours)

        chessboardEdge = cv2.approxPolyDP(largest, 0, True)
        mask = np.zeros_like(img_gray)
        cv2.fillConvexPoly(mask, chessboardEdge, 255, 1)
        extracted = np.zeros_like(img)
        extracted[mask == 255] = img[mask == 255]

        if debug:
            cv2.imshow('mask', extracted)

        canny = cv2.Canny(extracted, 10, 255)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        closed = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)
        closed = cv2.erode(closed, kernel, iterations=1)
        closed = cv2.dilate(closed, kernel, iterations=1)

        cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        c = sorted(cnts, key = cv2.contourArea, reverse = True)[1]
        peri = cv2.arcLength(c, True)
        edgeApprox = cv2.approxPolyDP(c, 0.1 * peri, True)

        imgContours = extracted.copy()
        img_gray = cv2.cvtColor(extracted, cv2.COLOR_BGR2GRAY)
        cv2.drawContours(imgContours, [edgeApprox], -1, (0,255,0), 2, cv2.LINE_AA)
        mask = np.zeros_like(img_gray)
        cv2.fillConvexPoly(mask, edgeApprox, 255, 1)
        extracted = np.zeros_like(img)
        extracted[mask == 255] = img[mask == 255]

        if debug:
            cv2.imshow('mask2', extracted)

        return extracted

    def detectEdges(self, image):
        blur = cv2.medianBlur(image, 3)
        # Detect edges
        edges = cv2.Canny(blur, 50, 250)
        colorEdges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        if debug:
            cv2.imshow('Canny', edges)

        return edges, colorEdges

    def detectLines(self, edges, colorEdges):
        # Make line bigger
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        edges = cv2.dilate(edges, None, iterations=1)
        # Detect lines
        lines = cv2.HoughLinesP(edges, 1,  np.pi / 180, 150, np.array([]), 200, 10)
        colorEdgesCopy = colorEdges.copy()
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(colorEdgesCopy, (x1,y1), (x2,y2), (0,255,0), 2)

        if debug:
            cv2.imshow('Lines', colorEdgesCopy)

        horizontal = []
        vertical = []
        for line in lines:
            [[x1, y1, x2, y2]] = line
            newLine = Line(x1, x2, y1, y2)
            if newLine.orientation == 'horizontal':
                horizontal.append(newLine)
            else:
                vertical.append(newLine)

        return horizontal, vertical

    def detectCorners(self, horizontal, vertical, colorEdges):
        corners = []
        for v in vertical:
            for h in horizontal:
                x, y = v.findIntersection(h)
                corners.append([x, y])

        # Remove duplicate corners
        rmvDupCorners = []
        for c in corners:
            matched = False
            for d in rmvDupCorners:
                if math.sqrt((d[0]-c[0])*(d[0]-c[0]) + (d[1]-c[1])*(d[1]-c[1])) < 20:
                    matched = True
                    break
            if not matched:
                rmvDupCorners.append(c)

        for c in rmvDupCorners:
            cv2.circle(colorEdges, (c[0],c[1]), 10, (0,0,255), 1, cv2.LINE_AA)

        if debug:
            cv2.imshow('Corners', colorEdges)

        return rmvDupCorners

    def detectSquares(self, corners, colorEdges):
        # Sort corners by row
        corners.sort(key=lambda x: x[0])
        rows = [[],[],[],[],[],[],[],[],[]]
        r = 0
        for c in range(81):
            if c > 0 and c % 9 == 0:
                r += 1
            rows[r].append(corners[c])

        letters = ['a','b','c','d','e','f','g','h']
        numbers = ['1','2','3','4','5','6','7','8']
        squares = []

        # Sort corners by column
        for r in rows:
            r.sort(key=lambda y: y[1])

        # Init squares
        for r in range(8):
            for c in range(8):
                c1 = rows[r][c]
                c2 = rows[r][c+1]
                c3 = rows[r+1][c+1]
                c4 = rows[r+1][c]

                position = letters[r] + numbers[7-c]
                newSquare = Square(colorEdges,c1,c2,c3,c4,position)
                newSquare.draw(colorEdges,(0,255,255),2)
                newSquare.drawROI(colorEdges,(255,0,0),2)
                newSquare.namedTheSquare(colorEdges)
                squares.append(newSquare)

        if debug:
            cv2.imshow('Squares', colorEdges)

        return squares
