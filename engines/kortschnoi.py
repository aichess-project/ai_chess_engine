import chess, os, logging
from ctypes import *
from engine_libs.config import Config
from engines.chess_engine import Chess_Engine
from engine_libs.log_lib import *

class Kortschnoi_Engine(Chess_Engine):
    def __init__(self, config, color, super_call = False):
        if not super_call:
          logging.info(START_INIT_ENGINE + COLOR_PARAM(color))
        super().__init__(config, color, True)
        if not super_call:
          self.who_am_i = "Kortschnoi"
          logging.info(END_INIT_ENGINE + ENGINE_PARAM(self.who_am_i))
          logging.info(CONFIG_LOG_ENTRY(config.get_start_pos(), self.nnue_net_filename, self.max_depth, self.extra_depth, False))

    def evaluation_fen_pos(self, fen_str, color):
      logging.info(START_EXT_EVAL + FEN_PARAM(fen_str) + COLOR_PARAM(color))
      eval = self.nnue.nnue_evaluate_fen(bytes(fen_str, encoding='utf-8'))/200.08
      if color == chess.BLACK:
        eval = -eval
      logging.info(END_EXT_EVAL + EVAL_PARAM(eval))
      return eval
    
    def evaluate_position(self):
      if self.board.is_checkmate():
        return float("-inf") if self.board.turn == chess.WHITE else float("inf")
      elif self.board.is_stalemate() or self.board.is_insufficient_material() or self.board.is_seventyfive_moves():
        return 0.0
      logging.info(START_GET_FEN)
      fen_str = self.board.fen()
      logging.info(END_GET_FEN)
      return self.evaluation_fen_pos(fen_str, self.board.turn)
    
    def last_move_has_priority(self):
        if self.board.is_capture() or self.board.is_check():
            return True
        return False

    def gen_moves(self):
      logging.info(START_GEN_MOVES)
      legal_moves =  list(self.board.legal_moves)
      logging.info(END_GEN_MOVES)
      return legal_moves

    def analyse_move(self, move, depth, maximize):
      is_capture = self.board.is_capture(move)
      self.board.push(move)
      logging.info(START_ANALYSE + MOVE_PARAM(move))
      eval = self.minimax(depth - 1, not maximize, is_capture)
      logging.info(END_ANALYSE + MOVE_PARAM(move) + EVAL_PARAM(eval))
      self.board.pop()
      return eval
       
    def find_best_move(self):
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
            eval = self.evaluate_position()
            logging.info(END_MINIMAX + DEPTH_PARAM(depth))
            return eval
        legal_moves = self.gen_moves()
        best_value = float("-inf") if maximize else float("inf")
        for move in legal_moves:
            value = self.analyse_move(move, depth, maximize)
            best_value = max(best_value, value) if maximize else min(best_value, value)
        logging.info(END_MINIMAX + DEPTH_PARAM(depth)+EVAL_PARAM(best_value))
        return best_value