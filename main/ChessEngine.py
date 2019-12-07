import chess
import chess.uci
import numpy as np
import stockfish
from Board import Board

class ChessEngine:
    '''
    Using python built-in chess engine to interacts with stockfish engine
    Interations through Universal Chess Interface protocol (UCI)
    Save game moves into txt file
    '''
    def __init__(self):
        self.engBoard = chess.Board()
        self.engine = chess.uci.popen_engine('./stockfish_10_x64')
        self.engine.uci()
        print(self.engBoard)

    def updateMove(self, move):
        uciMove = chess.Move.from_uci(move)

        if uciMove not in self.engBoard.legal_moves:
            return 1
        else:
            self.engBoard.push(uciMove)
            print(self.engBoard)
            return 0

    def feedToAI(self):
        self.engine.position(self.engBoard)

        response = self.engine.go(movetime=2000)
        bestMove = response[0]

        self.engBoard.push(bestMove)

        f = open('./Gamelog/Game.txt', 'a+')
        f.write(bestMove.uci() + '\r\n')
        f.close()

        print(self.engBoard)

        return bestMove
