from engines.kortschnoi import Kortschnoi_Engine
from engine_libs.config import Config
import chess

if __name__ == '__main__':
    conf = Config("/Users/littlecapa/GIT/python/chess_engines/arena/config.yaml")
    engine_class = conf.get_engine_class(chess.WHITE)
    engine = globals()[engine_class](conf, chess.WHITE)
    board = engine.board
    
    # List of FEN positions
    fen_positions = [
        # e4
        "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
        # e4 e5
        "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 1",
        # e4 e6
        "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1",
        # e4 e6 Lc4
        "rnbqkbnr/pppp1ppp/4p3/8/2B1P3/8/PPPP1PPP/RNBQK1NR b KQkq - 0 1",
        # e4 e6 Lc4 Ke7
        "rnbq1bnr/ppppkppp/4p3/8/2B1P3/8/PPPP1PPP/RNBQK1NR w KQ - 0 1",
        # d4
        "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1",
        # d4 e5
        "rnbqkbnr/pppp1ppp/8/4p3/3P4/8/PPP1PPPP/RNBQKBNR w KQkq e6 0 1",
        # d4 d5
        "rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq d6 0 1",
    ]

    # Iterate through the list of FEN positions
    for pos in fen_positions:
        board.set_fen(pos)
        print(f"Processing FEN: {pos}, EVAL: {engine.evaluate_position()} {board.turn}")
