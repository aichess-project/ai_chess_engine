import chess, logging
from engines.minmax import MinMax_Engine
from config.net_config import create_net

class KRK_MINMAX_Engine(MinMax_Engine):
    
    def __init__(self, config, board, max_depth = 3, pgn_logging = False):
        super().__init__(config, board, max_depth, pgn_logging)
        self.configure_eval(config)

    def configure_eval(self, config):
        self.machine = create_net(config["model_config_file"])
        self.machine.load_model(config["model_load_file"])
        self.converter = config["converter"]
       
    def convert_fen2x(self, fen):
        x = self.converter(fen)
        return x

    def evaluate_fen_pos(self, fen):
        y = self.machine(self.convert_fen2x(fen)).item() * -1
        logging.debug(f"Y: {y} Turn: {self.board.turn}")
        if y > 0:
            y = 50 - y
        elif y < 0:
            y = -50 -y
        return y