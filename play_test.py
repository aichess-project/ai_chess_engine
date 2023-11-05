from engine_libs.log_lib import setup_logging
from engine_libs.config import Config
from ui.ui import ChessUI
from engines.kortschnoi import Kortschnoi_Engine
import chess

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
                _, exit = ui.get_move_and_execute(board)
            else:
                best_move, value = white_engine.find_best_move()
                print(f"Best Move: {best_move} ({value})")
                board.push(best_move)

            if board.is_game_over() or exit:
                break

            if human == chess.BLACK:
                ui.print_board(board)        
                _, exit = ui.get_move_and_execute(board)
            else:
                best_move, value = black_engine.find_best_move()
                print(f"Best Move: {best_move} ({value})")
                board.push(best_move)
            
            if human is None:
                ui.print_board(board)   

        print("Game over. Result: " + board.result())
        board = board_copy

if __name__ == "__main__":
    setup_logging()
    conf = Config("/Users/littlecapa/GIT/python/chess_engines/arena/config_test.yaml")
    play(conf)