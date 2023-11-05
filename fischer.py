import chess, os, logging
from ctypes import *
from engine_libs.config import Config
from engines.kortschnoi import Kortschnoi_Engine
from engine_libs.log_lib import *

class Fischer_Engine(Kortschnoi_Engine):
    def __init__(self, config, color, super_call = False):
        if not super_call:
          logging.info(START_INIT_ENGINE + COLOR_PARAM(color))
        super().__init__(config, color, True)
        if not super_call:
          self.who_am_i = "Fischer"
          logging.info(END_INIT_ENGINE + ENGINE_PARAM(self.who_am_i))
          logging.info(CONFIG_LOG_ENTRY(config.get_start_pos(), self.nnue_net_filename, self.max_depth, self.extra_depth, False))
    
    def alpha_beta(self, depth, alpha, beta, maximize, is_capture):
        logging.info(START_ALPHABETA + DEPTH_PARAM(depth) + MAXIMIZE_PARAM(maximize))
        if depth <= -self.extra_depth or (depth <= 0 and not (is_capture or self.board.is_check())) or self.board.is_game_over():
            eval = self.evaluate_position()
            logging.info(END_ALPHABETA + DEPTH_PARAM(depth) + EVAL_PARAM(eval) + MOVE_PARAM(""))
            return eval, None

        legal_moves = self.gen_moves()
        best_value = float("-inf") if maximize else float("inf")
        best_move = None
        alpha_beta_break = False

        for move in legal_moves:
            capture = self.board.is_capture(move)
            self.board.push(move)
            value, _ = self.alpha_beta(depth - 1, -beta, -alpha, not maximize, capture)
            #value = -value
            self.board.pop()

            if maximize:
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, value)
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, value)

            if alpha >= beta:
                alpha_beta_break = True
                break

        logging.info(END_ALPHABETA + DEPTH_PARAM(depth)+EVAL_PARAM(best_value)+MOVE_PARAM(best_move)+ALPHA_BETA_BREAK_PARAM(alpha_beta_break))
        return best_value, best_move

    def find_best_move(self):
        start_fen = self.board.fen()
        logging.info(START_FIND_BEST + ENGINE_PARAM(self.who_am_i) + FEN_PARAM(start_fen))
        best_value, best_move = self.alpha_beta(self.max_depth, float("-inf"), float("inf"), self.board.turn, False)
        logging.info(END_FIND_BEST + ENGINE_PARAM(self.who_am_i) + MOVE_PARAM(best_move) + EVAL_PARAM(best_value))
        return best_move, best_value
