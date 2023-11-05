import chess

from engine_libs.config import Config

conf = Config("/Users/littlecapa/GIT/python/chess_engines/arena/config.yaml")

print(conf.get_color(chess.WHITE))
print(conf.get_color(chess.BLACK))

print(conf.is_engine(chess.WHITE))
print(conf.is_engine(chess.BLACK))

print(conf.get_nnue_info(chess.WHITE))
print(conf.get_nnue_info(chess.BLACK))

print(conf.get_max_depth(chess.WHITE))
print(conf.get_max_depth(chess.BLACK))

print(conf.get_extra_depth(chess.WHITE))
print(conf.get_extra_depth(chess.BLACK))


print(conf.get_stats())
print(conf.get_stats_append())
print(conf.get_stats_raw_file())
print(conf.get_start_pos())
print(conf.get_nr_games())
