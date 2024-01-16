import chess, logging
from engines.chess_engine import Chess_Engine

MAX_VALUE = 999999.0

class MinMax_Engine(Chess_Engine):
    
    def __init__(self, config, board, max_depth = 3, pgn_logging = False):
        super().__init__(config, board, max_depth, pgn_logging)

    def configure_eval(self, config):
        raise Exception("Not implemented")
       
    def convert_fen2x(self, fen):
        raise Exception("Not implemented")

    def evaluate_fen_pos(self, fen):
       raise Exception("Not implemented")
    
    def evaluate_position(self, depth):
        # Evaluate the current state of the board
        if self.board.is_checkmate():
            distance = self.max_depth - depth
            eval = (-MAX_VALUE + distance) if self.board.turn else (MAX_VALUE - distance)  # Checkmate, return a very low or high score
        elif self.board.is_stalemate() or self.board.is_insufficient_material():
            eval = 0  # Stalemate or insufficient material, the game is a draw
        else:
            eval = self.evaluate_fen_pos(self.board.fen())
        self.add_eval(eval)
        return eval

    def find_best_move(self):
        super().find_best_move()
        best_move = None
        maximize = self.board.turn
        best_value = float("-inf") if maximize else float("inf")
        legal_moves = list(self.board.legal_moves)
        best_move = legal_moves[0]
        for move in legal_moves:
            self.push_move(move)
            value = self.minimax(self.max_depth - 1, not maximize)
            self.add_eval(value)
            self.pop_move()
            if maximize:
              if value > best_value:
                best_value = value
                best_move = move
            else:
              if value < best_value:
                best_value = value
                best_move = move
        self.found_best_move(best_move, best_value)
        return best_move, best_value

    def minimax(self, depth, maximize):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_position(depth)
        legal_moves = list(self.board.legal_moves)
        best_value = float("-inf") if maximize else float("inf")
        for move in legal_moves:
            self.push_move(move)
            value = self.minimax(depth - 1, not maximize)
            best_value = max(best_value, value) if maximize else min(best_value, value)
            self.add_eval(best_value)
            self.pop_move()
        return best_value
