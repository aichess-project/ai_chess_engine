import chess, os, logging
from ctypes import *
from engine_libs.config import Config
from engines.fischer import Fischer_Engine
from cachetools import cached, LRUCache, TTLCache, LFUCache
from engine_libs.log_lib import *

class Young_Bobby_Engine(Fischer_Engine):
    
    def __init__(self, config, color, super_call = False):
        if not super_call:
            logging.info(START_INIT_ENGINE + COLOR_PARAM(color))
        super().__init__(config, color, True)
        self.cache_size = config.get_cache_size(self.color)
        if not super_call:
            self.who_am_i = "Young_Bobby"
            logging.info(END_INIT_ENGINE + ENGINE_PARAM(self.who_am_i))
            logging.info(CONFIG_LOG_ENTRY(config.get_start_pos(), self.nnue_net_filename, self.max_depth, self.extra_depth, True))
    
    #@cached(cache=LRUCache(maxsize=1000))
    @cached(cache=LFUCache(maxsize=10000))
    def evaluation_fen_pos(self, fen_str, color):
        return super().evaluation_fen_pos(fen_str, color)