import chess, logging
from engines.minmax import MinMax_Engine
from libs.syzygy_lib import Syzygy_Lib

class KRK_MINMAX_TB_Engine(MinMax_Engine):
    
    def __init__(self, config, board, max_depth = 1, pgn_logging = False):
        super().__init__(config, board, max_depth, pgn_logging)
        self.sl = Syzygy_Lib(SYZYGY_PATH = config["syzygy_path"])

    def evaluate_fen_pos(self, fen):
        _, eval = self.sl.position_dist_mate(self.board)
        if self.board.turn == chess.BLACK:
            eval = -eval
        if eval != 0:
            eval = 50 - eval
        return eval