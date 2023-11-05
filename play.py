from engine_libs.log_lib import *
from engine_libs.config import Config
from ui.ui import ChessUI
from engines.kortschnoi import Kortschnoi_Engine
from engines.fischer import Fischer_Engine
from engines.young_victor import Young_Victor_Engine
from engines.young_bobby import Young_Bobby_Engine
import chess, logging
import datetime

def play(conf):
    ui = ChessUI()

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
    board_copy = board

    for _ in range(conf.get_nr_games()):
        exit = False
        while not board.is_game_over() and exit == False:
            if human == chess.WHITE:
                ui.print_board(board)        
                exit, user_move = ui.get_move_and_execute(board)
                if not exit:
                    logging.info(EXEC_STRING + MOVE_PARAM(user_move))
            else:
                best_move, value = white_engine.find_best_move()
                print(f"Best Move: {best_move} ({value}) ({datetime.now()})")
                board.push(best_move)
                logging.info(EXEC_STRING + MOVE_PARAM(best_move) + EVAL_PARAM(value))

            if board.is_game_over() or exit:
                break
            if human == chess.BLACK:
                ui.print_board(board)        
                exit, user_move = ui.get_move_and_execute(board)
                if not exit:
                    logging.info(EXEC_STRING + MOVE_PARAM(user_move))
            else:
                best_move, value = black_engine.find_best_move()
                print(f"Best Move: {best_move} ({value}) ({datetime.now()})")
                board.push(best_move)
                logging.info(EXEC_STRING + MOVE_PARAM(best_move) + EVAL_PARAM(value))
            
            if human is None:
                ui.print_board(board)   

        print("Game over. Result: " + board.result())
        board = board_copy

if __name__ == "__main__":
    setup_logging()
    conf_file = "/Users/littlecapa/GIT/python/chess_engines/arena/config.yaml"
    logging.debug(f"conf_file = {conf_file}")
    conf = Config(conf_file)
    play(conf)