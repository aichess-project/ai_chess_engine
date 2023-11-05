from engine_libs.log_lib import *
from engine_libs.config import Config
from engine_libs.fen_lib import remove_counters_from_fen
from engines.tal import Tal_Engine
from engines.kortschnoi import Kortschnoi_Engine
from engines.young_victor import Young_Victor_Engine
import chess, logging, random
from datetime import datetime, timedelta
import pandas as pd



def play(conf, with_counter = False):

    white_engine_class = conf.get_engine_class(chess.WHITE)
    white_engine_name = white_engine_class.replace("_Engine", "")
    white_engine_name = white_engine_name.replace("_", " ")
    black_engine_class = conf.get_engine_class(chess.BLACK)
    black_engine_name = black_engine_class.replace("_Engine", "")
    black_engine_name = black_engine_name.replace("_", " ")
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

    file = "./test_data/fen_eval.csv"

    # Read the CSV file into a Pandas DataFrame
    eval_df = pd.read_csv(file, delimiter = ",")

    for color in {chess.WHITE, chess.BLACK}:
        if color == chess.WHITE:
            engine_name = "Kortschnoi"
            engine = white_engine
            color_str = "White"
        else:
            engine_name = "Young Victor"
            engine = black_engine
            color_str = "Black"

        start_time = datetime.now()
        counter = 0
        for _, row in eval_df.iterrows():
            if row['ENGINE'] == engine_name:
                fen = row['FEN']
                if with_counter == False:
                    fen = remove_counters_from_fen(fen)
                _ = engine.evaluation_fen_pos(fen, color)
                counter += 1
        duration = datetime.now() - start_time
        
        print(f"Engine: {engine_name} Color: {color_str} Duration: {duration} Counter: {counter}")

if __name__ == "__main__":
    setup_logging()
    #conf_file = "/Users/littlecapa/GIT/python/chess_engines/arena/config_kortschnoi.yaml"
    conf_file = "/Users/littlecapa/GIT/python/chess_engines/arena/config_tal.yaml"
    logging.debug(f"conf_file = {conf_file}")
    conf = Config(conf_file)
    play(conf, with_counter = False)