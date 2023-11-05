from engine_libs.log_lib import *
from engine_libs.config import Config

from engines.kortschnoi import Kortschnoi_Engine
from engines.young_victor import Young_Victor_Engine
import chess, logging, random
from datetime import datetime, timedelta


def play(conf):

    white_engine_class = conf.get_engine_class(chess.WHITE)
    black_engine_class = conf.get_engine_class(chess.BLACK)
    board = None
    human = None
    if white_engine_class != "":
        white_engine = globals()[white_engine_class](conf, chess.WHITE)
        board = white_engine.board
    else:
        human = chess.WHITE

    if black_engine_class != "":
        black_engine = globals()[black_engine_class](conf, chess.BLACK)
        if board is None:
            board = black_engine.board
        else:
            black_engine.board = board
    else:
        human = chess.BLACK

    fen_list = []

    max = 100000
    with open("./test_data/fen_list_KRK.txt", 'r') as fen_file:
        nr = 0
        for line in fen_file:
            fen_list.append(line)
            nr += 1
            if nr > max:
                break

    for color in {chess.WHITE, chess.BLACK}:
        if human == color: 
            break
        if color == chess.WHITE:
            engine = white_engine
        else:
            engine = black_engine

        print(engine.who_am_i)

        start_time = datetime.now()
        for i in range(10):
            random.shuffle(fen_list)
            nr = 0         
            for fen_str in fen_list:
                _ = engine.evaluation_fen_pos(fen_str, color)
                current_time = datetime.now()
                duration = current_time - start_time
            print(f"Color: {color} Iteration: {i} Duration {duration}")
            nr += 1
            if nr > max / 10:
                break
        print(f"Color: {color} Duration {duration}")

if __name__ == "__main__":
    setup_logging()
    conf_file = "/Users/littlecapa/GIT/python/chess_engines/arena/config.yaml"
    logging.debug(f"conf_file = {conf_file}")
    conf = Config(conf_file)
    play(conf)