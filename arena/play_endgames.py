import sys
sys.path.append('C:\\Users\\littl\\Documents\\GIT\\AI\\chess_engines')

import chess, logging
from datetime import datetime
from libs.chess_lib import Chess_Lib
from engines.krk_minmax import KRK_MINMAX_Engine
from engines.krk_minmax_tb import KRK_MINMAX_TB_Engine
from libs.log_lib import setup_logging

def play(fen):
    board = chess.Board(fen)
    print(board)
    print("Start:")
    config = {
        'model_config_file': r'C:\Users\littl\Documents\GIT\AI\pytorch_chess_trainer\manager\config\net_config_win_bm.yaml',
        'model_load_file': r'C:\Users\littl\Documents\GIT\AI\pytorch_chess_trainer\manager\Chess-Net_ChatGPT_Version_0.2.pth', 
        'converter': Chess_Lib.get_krk_bitmaps,
    }

    config_tb = {
        "syzygy_path" : r"C:\Users\littl\TableBases",
    }

    white_engine = KRK_MINMAX_Engine(board=board, config=config, max_depth=3, pgn_logging=False)
    black_engine = KRK_MINMAX_TB_Engine(board=board, config=config_tb)
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            best_move, value = white_engine.find_best_move()
        else:
            best_move, value = black_engine.find_best_move()
        logging.info(f"Best Move: {best_move} ({value}) ({datetime.now()})")
        board.push(best_move)

    logging.info("Game over. Result: " + board.result())
    logging.info(board)

if __name__ == "__main__":
    setup_logging()
    fen_list = ["8/8/8/4k3/8/8/R7/K7 b - - 0 1", "8/8/8/8/4R3/5K1k/8/8 w - - 0 1", "8/8/8/8/1K1R4/8/k7/8 b - - 0 1"]
    for fen in fen_list:
        play(fen)