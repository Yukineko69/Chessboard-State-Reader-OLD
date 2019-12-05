import chess
import chess.uci
import numpy as np
import stockfish
from Board import Board

class ChessEngine:
    def __init__(self):
        self.engBoard = chess.Board()
        self.engine = chess.uci.popen_engine('./stockfish_10_x64')
        self.engine.uci()
        print(self.engBoard)
