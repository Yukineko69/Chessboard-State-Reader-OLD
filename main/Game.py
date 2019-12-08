import imutils
import cv2
import argparse
import chess
from ChessEngine import ChessEngine
from BoardRecognition import BoardRecognition
from Board import Board
from Camera import Camera


class Game:
    '''
    Holds the whole game information
    Interacting with Board and Chess Engine
    '''
    def __init__(self, url):
        self.over = False
        self.CPUMoveError = False
        self.PlayerMoveError = False
        self.isCheck = False
        self.winner = "Me"
        self.url = url

    def setUp(self):
        self.camera = Camera(self.url)
        self.chessEngine = ChessEngine()
        self.board = 0
        self.current = 0
        self.previous = 0
        self.CPULastMove = "0"

    def analyzeBoard(self):
        boardRec = BoardRecognition(self.camera)
        self.board = boardRec.initializeBoard()
        self.board.assignState()

    def checkBoardIsSet(self):
        self.current = self.camera.takePicture()

        cv2.imwrite('./ProcessImage/SetUpBoard.jpg', self.current)

    def playerMove(self):
        self.previous = self.current
        self.current = self.camera.takePicture()
        # self.current = self.camera.takePicture4()
        move = self.board.determineChanges(self.previous, self.current)

        # # Test
        # move = 'd7d5'

        code = self.chessEngine.updateMove(move)
        print('Your move:', move)
        # print('code:', code)
        # print('PlayerMoveError:', self.PlayerMoveError)

        if code == 1:
            # Illegal move
            self.PlayerMoveError = True
        else:
            self.PlayerMoveError = False
            f = open('./Gamelog/Game.txt', 'a+')
            f.write(chess.Move.from_uci(move).uci() + '\r\n')
            f.close()
        # Check game over
        if self.chessEngine.engBoard.is_checkmate():
            self.winner = 'You win'
            self.over = True

    def playerPromotion(self, move):
        print(move)
        code = self.chessEngine.updateMove(move)

        if code == 1:
            # Illegal
            print('Error')
            self.PlayerMoveError = True
        else:
            self.PlayerMoveError = False
            f = open('./Gamelog/Game.txt', 'a+')
            f.write(chess.Move.from_uci(move).uci() + '\r\n')
            f.close()

        if self.chessEngine.engBoard.is_checkmate():
            self.winner = 'You win'
            self.over = True

    def CPUMove(self):
        self.CPULastMove = self.chessEngine.feedToAI()
        self.isCheck = self.chessEngine.engBoard.is_check()

        copy = self.current.copy()
        if len(self.CPULastMove.uci()) == 4:
            position1 = self.CPULastMove.uci()[:2]
            position2 = self.CPULastMove.uci()[2:]
            CPUMoveSquares = []

            for square in self.board.squares:
                if square.position == position1 or square.position == position2:
                    CPUMoveSquares.append(square)

            CPUMoveSquares[0].draw(copy, (255,0,0), 2)
            CPUMoveSquares[1].draw(copy, (255,0,0), 2)
            cv2.imwrite('./ProcessImage/CPUMove.jpg', copy)

        if self.chessEngine.engBoard.is_checkmate():
            self.winner = 'CPU win'
            self.over = True

        return self.CPULastMove

    def updateCurrent(self):
        self.previous = self.current
        self.current = self.camera.takePicture()
        # self.current = self.camera.takePicture3()

        move = self.board.determineChanges(self.previous, self.current)
        move = chess.Move.from_uci(move)

        # move = chess.Move.from_uci('e2e4')
        # # Test
        print('Your move for cpu:', move)
        print('Cpu move:', self.CPULastMove)
        # print('CPUMoveError:', self.CPUMoveError)


        # Check if player moved CPU piece correctly
        if move == self.CPULastMove:
            self.CPUMoveError = False
        else:
            self.CPUMoveError = True
