import chess, chess.pgn, logging
from ctypes import *
from engine_libs.config import Config
from engine_libs.log_lib import *
import logging

class NodeStack:
    def __init__(self):
        self.stack = []

    def push(self, node):
        self.stack.append(node)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            raise IndexError("pop from an empty stack")

    def top(self):
        if not self.is_empty():
            return self.stack[-1]
        else:
            return None

    def size(self):
        return len(self.stack)

    def is_empty(self):
        return len(self.stack) == 0

class Chess_Engine():
    def __init__(self, config, board, max_depth = 3, pgn_logging = False):
        self.board = board
        self.max_depth = max_depth
        self.pgn_logging = pgn_logging

    def find_best_move(self):
        if self.pgn_logging:
            self.log_game = chess.pgn.Game()
            self.log_game.headers["FEN"] = self.board.fen()
            self.nodes = NodeStack()

    def found_best_move(self, move, eval):
        if self.pgn_logging:
            logging.info(f"Best Move: {move} Eval: {eval}")
            logging.info(f"LOG PGN: {str(self.log_game)}")

    def push_move(self, move):
        if self.pgn_logging:
            if self.nodes.is_empty():
                node = self.log_game.add_variation(move)
            else:
                node = self.nodes.top().add_variation(move)
            self.nodes.push(node)
        self.board.push(move)

    def pop_move(self):
        if self.pgn_logging:
            self.nodes.pop()
        self.board.pop()

    def add_eval(self, eval):
        if self.pgn_logging:
            if not self.nodes.is_empty():
                self.nodes.top().comment = f"Eval: {eval}"
