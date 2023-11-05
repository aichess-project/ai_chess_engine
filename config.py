import yaml
import os
import chess

class Config:

    def __init__(self, config_filename = "config.yaml"):
        with open(config_filename, "r") as f:
            self.config_data = yaml.safe_load(f)

    def get_color(self, color):
        if color == chess.WHITE:
            return "WHITE"
        elif color == chess.BLACK:
            return "BLACK"
        return ""

    def is_engine(self, color):
        return not self.config_data["ENGINE"][self.get_color(color)]["HUMAN"]

    def get_nnue_info(self, color):
        data = self.config_data["ENGINE"][self.get_color(color)]
        if "NNUE" in data:
            lib = self.config_data["ENGINE"][self.get_color(color)]["NNUE"]["LIB"]
            net = self.config_data["ENGINE"][self.get_color(color)]["NNUE"]["NET"]
            return lib, net
        return "", ""
    
    def get_max_depth(self, color):
        if self.is_engine(color):
            return self.config_data["ENGINE"][self.get_color(color)]["MAX_DEPTH"]
        else:
            return 0
    
    def get_extra_depth(self, color):
        if self.is_engine(color):
            return self.config_data["ENGINE"][self.get_color(color)]["EXTRA_DEPTH"]
        else:
            return 0
        
    def get_cache_size(self, color):
        if self.is_engine(color):
            return self.config_data["ENGINE"][self.get_color(color)]["CACHE_SIZE"]
        else:
            return 0
        
    def get_engine_class(self, color):
        if self.is_engine(color):
            return self.config_data["ENGINE"][self.get_color(color)]["ENGINE_CLASS"]
        else:
            return ""
    
    def get_stats(self, color):
        if self.is_engine(color):
            return self.config_data["STATS"][self.get_color(color)]["DO_STATS"]
        else:
            return ""
    
    def get_pgn(self, color):
        if self.is_engine(color):
            return self.config_data["STATS"][self.get_color(color)]["DO_PGN"]
        else:
            return ""
    
    def get_stats_append(self, color):
        if self.is_engine(color):
            return self.config_data["STATS"][self.get_color(color)]["APPEND"]
        else:
            return ""
    
    def get_stats_raw_file(self, color):
        if self.is_engine(color):
            return self.config_data["STATS"][self.get_color(color)]["RAW_FILE"]
        else:
            return ""
        
    def get_stats_pgn_file(self, color):
        if self.is_engine(color):
            return self.config_data["STATS"][self.get_color(color)]["PGN_FILE"]
        else:
            return ""
    
    def get_start_pos(self):
        return self.config_data["MATCH"]["START_POS"]
    
    def get_nr_games(self):
        return self.config_data["MATCH"]["NUMBER_GAMES"]
