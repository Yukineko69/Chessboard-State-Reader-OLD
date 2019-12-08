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
    '''
    Holds all Squares objects and updates changes to them after every move
    '''
    def __init__(self, squares):
        self.squares = squares
        self.boardMatrix = []
        self.promotion = 'q'
        self.promo = False
        self.move = 'e2e4'

    def draw(self, image):
        for square in self.squares:
            square.draw(image, (0,255,255))
            square.namedTheSquare(image)

    def assignState(self):
        black = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        white = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']

        # Assign board state row by row
        for i in range(8):
            self.squares[8*i + 0].state = black[i]
            self.squares[8*i + 1].state = 'p'
            self.squares[8*i + 2].state = '.'
            self.squares[8*i + 3].state = '.'
            self.squares[8*i + 4].state = '.'
            self.squares[8*i + 5].state = '.'
            self.squares[8*i + 6].state = 'P'
            self.squares[8*i + 7].state = white[i]

        for square in self.squares:
            self.boardMatrix.append(square.state)

    def determineChanges(self, previous, current):
        copy = current.copy()

        largestSquare = self.squares[0]
        secondLargestSquare = self.squares[0]
        largestDist = 0
        secondLargestDist = 0
        stateChange = []

        # Check for differences in color between the photos
        for sq in self.squares:
            colorPrevious = sq.roiColor(previous)
            colorCurrent = sq.roiColor(current)

            # Distance in bgr values
            sum = 0
            for i in range(3):
                sum += (colorCurrent[i] - colorPrevious[i])**2

            distance = math.sqrt(sum)

            if distance > 25:
                stateChange.append(sq)

            if distance > largestDist:
                # Update squares with largest change in color
                secondLargestSquare = largestSquare
                secondLargestDist = largestDist
                largestDist = distance
                largestSquare = sq

            elif distance > secondLargestDist:
                # Update squares with second largest change in color
                secondLargestDist = distance
                secondLargestSquare = sq

        if  len(stateChange)  == 4:

            # If four square have color change in a single move, check if it a castling
            squareOne = stateChange[0]
            squareTwo = stateChange[1]
            squareThree = stateChange[2]
            squareFour = stateChange[3]

            # Check White short side castle
            if squareOne.position == 'e1' or squareTwo.position == 'e1' or squareThree.position == 'e1' or  squareFour.position == 'e1':
                if squareOne.position == 'f1'  or squareTwo.position == 'f1' or squareThree.position == 'f1'  or squareFour.position == 'f1':
                    if squareOne.position == 'g1' or squareTwo.position == 'g1' or squareThree.position == 'g1' or  squareFour.position == 'g1':
                        if squareOne.position == 'h1'  or squareTwo.position == 'h1' or squareThree.position == 'h1'  or squareFour.position == 'h1':
                            self.move = 'e1g1'
                            print(self.move)
                            if debug:
                                squareOne.draw(copy, (255,0,0), 2)
                                squareTwo.draw(copy, (255,0,0), 2)
                                squareThree.draw(copy, (255,0,0),2)
                                squareFour.draw(copy, (255,0,0), 2)
                                cv2.imshow('previous', previous)
                                cv2.imshow('identified', copy)

                            return self.move

                # Check White long side castle
                if squareOne.position == 'd1'  or squareTwo.position == 'd1' or squareThree.position == 'd1'  or squareFour.position == 'd1':
                    if squareOne.position == 'c1'  or squareTwo.position == 'c1' or squareThree.position == 'c1'  or squareFour.position == 'c1':
                        if squareOne.position == 'a1'  or squareTwo.position == 'a1' or squareThree.position == 'a1'  or squareFour.position == 'a1':

                            self.move = 'e1c1'
                            print(self.move)
                            if debug:
                                squareOne.draw(copy, (255,0,0), 2)
                                squareTwo.draw(copy, (255,0,0), 2)
                                squareThree.draw(copy, (255,0,0),2)
                                squareFour.draw(copy, (255,0,0), 2)
                                cv2.imshow('previous', previous)
                                cv2.imshow('identified', copy)

                            return self.move

            # Check Black short side castle
            if squareOne.position == 'e8' or squareTwo.position == 'e8' or squareThree.position == 'e8' or  squareFour.position == 'e8':
                if squareOne.position == 'f8'  or squareTwo.position == 'f8' or squareThree.position == 'f8'  or squareFour.position == 'f8':
                    if squareOne.position == 'g8' or squareTwo.position == 'g8' or squareThree.position == 'g8' or  squareFour.position == 'g8':
                        if squareOne.position == 'h8'  or squareTwo.position == 'h8' or squareThree.position == 'h8'  or squareFour.position == 'h8':
                            self.move = 'e8g8'
                            print(self.move)
                            if debug:
                                squareOne.draw(copy, (255,0,0), 2)
                                squareTwo.draw(copy, (255,0,0), 2)
                                squareThree.draw(copy, (255,0,0),2)
                                squareFour.draw(copy, (255,0,0), 2)
                                cv2.imshow('previous', previous)
                                cv2.imshow('identified', copy)

                            return self.move

                # Check Black long side castle
                if squareOne.position == 'd8'  or squareTwo.position == 'd8' or squareThree.position == 'd8'  or squareFour.position == 'd8':
                    if squareOne.position == 'c8'  or squareTwo.position == 'c8' or squareThree.position == 'c8'  or squareFour.position == 'c8':
                        if squareOne.position == 'a8'  or squareTwo.position == 'a8' or squareThree.position == 'a8'  or squareFour.position == 'a8':

                            self.move = 'e8c8'
                            print(self.move)
                            if debug:
                                squareOne.draw(copy, (255,0,0), 2)
                                squareTwo.draw(copy, (255,0,0), 2)
                                squareThree.draw(copy, (255,0,0),2)
                                squareFour.draw(copy, (255,0,0), 2)
                                cv2.imshow('previous', previous)
                                cv2.imshow('identified', copy)

                            return self.move

        # Regular move with two squares change state
        squareOne = largestSquare
        squareTwo = secondLargestSquare

        if debug:
            squareOne.draw(copy, (255,0,0), 2)
            squareTwo.draw(copy, (255,0,0), 2)
            cv2.imshow('previous', previous)
            cv2.imshow('identified', copy)

        squareOne.draw(copy, (255,0,0), 2)
        squareTwo.draw(copy, (255,0,0), 2)
        # cv2.imwrite('./ProcessImage/Previous.jpg', previous)
        cv2.imwrite('./ProcessImage/Identified.jpg', copy)

        # Get colors for each square from each photo
        oneCurrent = squareOne.roiColor(current)
        twoCurrent = squareTwo.roiColor(current)

        # Calculate distance from empty square color value
        sumCurrent1 = 0
        sumCurrent2 = 0
        for i in range(3):
            sumCurrent1 += (oneCurrent[i] - squareOne.emptyColor[i])**2
            sumCurrent2 += (twoCurrent[i] - squareTwo.emptyColor[i])**2

        distCurrent1 = math.sqrt(sumCurrent1)
        distCurrent2 = math.sqrt(sumCurrent2)

        if distCurrent1 < distCurrent2:
            # Square 1 is closer to empty color value so it's empty
            squareTwo.state = squareOne.state
            squareOne.state = '.'
            # Check for promotion of a pawn
            if squareTwo.state.lower() == 'p':
                if squareOne.position[1:2] == '2' and squareTwo.position[1:2] == '1':
                    self.promo = True
                if squareOne.position[1:2] == '7' and squareTwo.position[1:2] == '8':
                    self.promo = True

            self.move = squareOne.position + squareTwo.position

        else:
            # Square 2 is currently empty
            squareOne.state = squareTwo.state
            squareTwo.state = '.'
            # Check pawn promotion
            if squareOne.state.lower() == 'p':
                if squareOne.position[1:2] == '1' and squareTwo.position[1:2] == '2':
                    self.promo = True
                if squareOne.position[1:2] == '8' and squareTwo.position[1:2] == '7':
                    self.promo = True


            self.move = squareTwo.position + squareOne.position

        return self.move
