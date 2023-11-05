import chess, os, logging
from ctypes import *
from engine_libs.config import Config
from engine_libs.log_lib import *

class Chess_Engine():
    def __init__(self, config, color, super_call = False):
        if not super_call:
          logging.info(START_INIT_ENGINE + COLOR_PARAM(color))
        self.color = color
        self.board = chess.Board(config.get_start_pos())
        self.max_depth = config.get_max_depth(color)
        self.extra_depth = config.get_extra_depth(color)
        self.nnue_lib_filename, self.nnue_net_filename = config.get_nnue_info(color)
        if self.nnue_lib_filename != "":           
          self.nnue = cdll.LoadLibrary(self.nnue_lib_filename)
          self.nnue.nnue_init(self.nnue_net_filename.encode('utf-8'))
        else:
           self.nnue = None
        if not super_call:
          self.who_am_i = "Nobody"
          logging.info(END_INIT_ENGINE + ENGINE_PARAM(self.who_am_i))
          logging.info(CONFIG_LOG_ENTRY(config.get_start_pos(), self.nnue_net_filename, self.max_depth, self.extra_depth, False))

    def get_name(self):
       return self.who_am_i
    
    def find_best_move(self):
        raise NotImplementedError("This method is not yet implemented")