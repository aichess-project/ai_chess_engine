from engine_libs.config import Config
from engine_libs.stack import Stack
from datetime import datetime

import pandas as pd

class Engine_Logger():

    def __init__(self, config, color):
        self.color = color
        self.do_stats = config.get_stats(self.color)
        self.do_pgn = config.get_pgn(self.color)
        append = config.get_stats_append(self.color)
        if append:
            self.mode = "a"
            self.header = False
        else:
            self.mode = "w"
            self.Header = True
        self.raw_file = config.get_stats_raw_file(self.color)
        self.pgn_file = config.get_stats_pgn_file(self.color)
        self.init()

    def init(self):
        self.raw_data = pd.DataFrame()
        raw_columns = ["Timestamp", "Start", "End", "Operation", "FEN", "Move", "Eval", "Information"]
        self.raw_data = pd.DataFrame(columns = raw_columns)
        self.pgn_data = ""

    def add_raw_data(self, start, end, operation, fen ="", move = "", eval ="", information =""):
        new_row = {
            "Timestamp": datetime.now(), 
            "Start": start, 
            "End": end, 
            "Operation": operation, 
            "FEN": fen, 
            "Move": move,
            "Eval": eval,
            "Information": information
        }
        self.raw_data.loc[len(self.raw_data)] = new_row

    def write_files(self):
        self.raw_data.to_csv(self.raw_file, mode=self.mode, header=self.header, index=False)
        with open(self.pgn_file, mode = self.mode) as file:
            file.write(self.pgn_data)
            file.write("\n")

    EXT_EVAL = "EXT_EVAL"
    GEN_MOVES = "GEN_MOVES"
    FIND_BEST_MOVE = "FIND_BEST_MOVE"
    GET_FEN = "GET_FEN"


    def start_external_evaluation(self):
        self.add_raw_data(start = True, end = False, operation = Engine_Logger.EXT_EVAL)

    def end_external_evaluation(self):
        self.add_raw_data(start = False, end = True, operation = Engine_Logger.EXT_EVAL)

    def start_get_fen(self):
        self.add_raw_data(start = True, end = False, operation = Engine_Logger.GET_FEN)

    def end_end_get_fen(self):
        self.add_raw_data(start = False, end = True, operation = Engine_Logger.GET_FEN)
    
    def start_gen_moves(self, fen = ""):
        self.add_raw_data(start = True, end = False, operation = Engine_Logger.GEN_MOVES, fen = fen)

    def end_gen_moves(self, fen = ""):
        self.add_raw_data(start = False, end = True, operation = Engine_Logger.GEN_MOVES, fen = fen)

    def start_find_best_move(self, fen = ""):
        self.init()
        self.add_raw_data(start = True, end = False, operation = Engine_Logger.FIND_BEST_MOVE, fen = fen)

    def end_find_best_move(self, fen = ""):
        self.add_raw_data(start = False, end = True, operation = Engine_Logger.FIND_BEST_MOVE, fen = fen)
        self.write_files()