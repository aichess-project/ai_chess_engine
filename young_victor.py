import chess, os, logging
from ctypes import *
from engine_libs.config import Config
from engines.kortschnoi import Kortschnoi_Engine
from engine_libs.eval_cache_hash import EvaluationHashCache
from engine_libs.log_lib import *

class Young_Victor_Engine(Kortschnoi_Engine):
    
    def __init__(self, config, color, super_call = False):
        if not super_call:
            logging.info(START_INIT_ENGINE + COLOR_PARAM(color))
        super().__init__(config, color, True)
        self.eval_cache = EvaluationHashCache(cache_size=config.get_cache_size(self.color), nnue = self.nnue)
        if not super_call:
            self.who_am_i = "Young_Victor"
            logging.info(END_INIT_ENGINE + ENGINE_PARAM(self.who_am_i))
            logging.info(CONFIG_LOG_ENTRY(config.get_start_pos(), self.nnue_net_filename, self.max_depth, self.extra_depth, True))
    
    
    def evaluate_position(self, depth):
      if self.board.is_checkmate():
        return float("-inf") if self.board.turn == chess.WHITE else float("inf")
      elif self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_seventyfive_moves():
        return 0.0
      logging.info(START_EXT_EVAL + DEPTH_PARAM(depth) + COLOR_PARAM(self.board.turn))
      eval = self.eval_cache.get_evaluation(depth)
      logging.info(END_EXT_EVAL + EVAL_PARAM(eval))
      return eval
    
    def analyse_move(self, move, depth, maximize):
      is_capture = self.board.is_capture(move)
      self.eval_cache.make_move(move, depth)
      logging.info(START_ANALYSE + MOVE_PARAM(move))
      eval = self.minimax(depth - 1, not maximize, is_capture)
      logging.info(END_ANALYSE + MOVE_PARAM(move) + EVAL_PARAM(eval))
      self.eval_cache.take_move_back()
      return eval
       
    def find_best_move(self):
        self.eval_cache.set_board(self.board)
        start_fen = self.board.fen()
        logging.info(START_FIND_BEST + ENGINE_PARAM(self.who_am_i) + FEN_PARAM(start_fen))
        best_move = None
        maximize = self.board.turn
        best_value = float("-inf") if maximize else float("inf")
        legal_moves = self.gen_moves()
        best_move = legal_moves[0]
        for move in legal_moves:
            value = self.analyse_move(move, self.max_depth, maximize)
            if maximize:
              if value > best_value:
                best_value = value
                best_move = move
            else:
              if value < best_value:
                best_value = value
                best_move = move
        logging.info(END_FIND_BEST + ENGINE_PARAM(self.who_am_i) + MOVE_PARAM(best_move) + EVAL_PARAM(value))
        return best_move, best_value

    def minimax(self, depth, maximize, is_capture):
        logging.info(START_MINIMAX + DEPTH_PARAM(depth))
        if depth <= -self.extra_depth or (depth <= 0 and not (is_capture or self.board.is_check())) or self.board.is_game_over():
            eval = self.evaluate_position(depth)
            logging.info(END_MINIMAX + DEPTH_PARAM(depth))
            return eval
        legal_moves = self.gen_moves()
        best_value = float("-inf") if maximize else float("inf")
        for move in legal_moves:
            value = self.analyse_move(move, depth, maximize)
            best_value = max(best_value, value) if maximize else min(best_value, value)
        logging.info(END_MINIMAX + DEPTH_PARAM(depth)+EVAL_PARAM(best_value))
        return best_value