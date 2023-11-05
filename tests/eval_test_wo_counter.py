from engine_libs.log_lib import *
from engine_libs.config import Config
from engine_libs.fen_lib import remove_counters_from_fen, get_color_from_fen
from engines.kortschnoi import Kortschnoi_Engine
import chess, logging, random
from datetime import datetime, timedelta
import pandas as pd



def play(conf):

    engine = Kortschnoi_Engine(conf, chess.WHITE)

    file = "./test_data/fen_eval.csv"

    # Read the CSV file into a Pandas DataFrame
    eval_df = pd.read_csv(file, delimiter = ",")

    for _, row in eval_df.iterrows():
        fen = row['FEN']
        fen_wo = remove_counters_from_fen(fen)
        color = get_color_from_fen(fen)

        print(fen)
        assert engine.evaluation_fen_pos(fen, color) == engine.evaluation_fen_pos(fen_wo, color)

if __name__ == "__main__":
    setup_logging()
    conf_file = "/Users/littlecapa/GIT/python/chess_engines/arena/config_tal.yaml"
    logging.debug(f"conf_file = {conf_file}")
    conf = Config(conf_file)
    play(conf)