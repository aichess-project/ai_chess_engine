import chess, os, logging
from ctypes import *
from engine_libs.config import Config
from engines.kortschnoi import Kortschnoi_Engine
from engine_libs.log_lib import *
from engine_libs.eval_cache_hash import EvaluationHashCache
#from engine_libs.eval_cache_dict import EvaluationCache

class Tal_Engine(Kortschnoi_Engine):
    
    def __init__(self, config, color, super_call = False):
        if not super_call:
            logging.info(START_INIT_ENGINE + COLOR_PARAM(color))
        super().__init__(config, color, True)
        self.cache_size = config.get_cache_size(self.color)
        if not super_call:
            self.who_am_i = "Tal"
            logging.info(END_INIT_ENGINE + ENGINE_PARAM(self.who_am_i))
            logging.info(CONFIG_LOG_ENTRY(config.get_start_pos(), self.nnue_net_filename, self.max_depth, self.extra_depth, True))
            self.cache = EvaluationHashCache()
    
    def evaluation_fen_pos(self, fen_str, color):
        eval, fen_hash = self.cache.get_evaluation(fen_str)
        if eval is not None:
            return eval
        eval = super().evaluation_fen_pos(fen_str, color)
        self.cache.add_evaluation(fen_hash, fen_str, eval)
        return eval