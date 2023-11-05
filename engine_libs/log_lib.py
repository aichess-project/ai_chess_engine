import logging
import chess

def setup_logging(level = logging.INFO):
    logging.basicConfig(
        filename='engine.log',  # Change this to your desired log file path
        level=logging.INFO,  # Change the log level as needed (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s.%(msecs)06f [%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

#
# Helper for LOG Structure
#
CONFIG_STRING = "CONFIG;"
START_STRING = "START;"
END_STRING = "END;"
EXEC_STRING = "EXECUTE;"
COLOR_STRING = "COLOR:"
EVAL_STRING = "EVAL:"
DEPTH_STRING = "DEPTH:"
FEN_STRING = "FEN:"
ENGINE_STRING = "ENGINE:"
MOVE_STRING = "MOVE:"
MAX_DEPTH_STRING = "MAX_DEPTH:"
EXTRA_DEPTH_STRING = "EXTRA_DEPTH:"
CACHE_STRING = "CACHE:"
MAXIMIZE_STRING = "MAXIMIZE:"
ALPHA_BETA_BREAK_STRING = "ALPHA_BETA_BREAK:"
OP_EXT_EVAL = "EXT_EVAL"
OP_GEN_MOVES = "GEN_MOVES"
OP_GET_FEN = "GET_FEN"
OP_ANALYSE = "ANALYSE"
OP_FIND_BEST = "FIND_BEST"
OP_MINIMAX = "MINIMAX"
OP_ALPHABETA = "ALPHABETA"
OP_INIT_ENGINE = "INIT_ENGINE"
START_EXT_EVAL = START_STRING + OP_EXT_EVAL + ";" 
END_EXT_EVAL = END_STRING + OP_EXT_EVAL + ";"
START_GEN_MOVES = START_STRING + OP_GEN_MOVES + ";"
END_GEN_MOVES = END_STRING + OP_GEN_MOVES + ";"
START_GET_FEN = START_STRING + OP_GET_FEN + ";"
END_GET_FEN = END_STRING + OP_GET_FEN + ";"
START_FIND_BEST = START_STRING + OP_FIND_BEST + ";"
END_FIND_BEST = END_STRING + OP_FIND_BEST + ";"
START_ANALYSE = START_STRING + OP_ANALYSE + ";"
END_ANALYSE = END_STRING + OP_ANALYSE + ";"
START_MINIMAX = START_STRING + OP_MINIMAX + ";"
END_MINIMAX = END_STRING + OP_MINIMAX + ";"
START_ALPHABETA = START_STRING + OP_ALPHABETA + ";"
END_ALPHABETA = END_STRING + OP_ALPHABETA + ";"
START_INIT_ENGINE = START_STRING + OP_INIT_ENGINE + ";"
END_INIT_ENGINE = END_STRING + OP_INIT_ENGINE + ";"

def get_start_string():
    return START_STRING.replace(";", "")

def get_end_string():
    return END_STRING.replace(";", "")

LOG_LINE_TYPES = [CONFIG_STRING.replace(";", ""), get_start_string(), get_end_string(), EXEC_STRING.replace(";", "")]
LOG_OP_TYPES = [OP_EXT_EVAL, OP_GEN_MOVES, OP_ANALYSE, OP_FIND_BEST, OP_MINIMAX, OP_INIT_ENGINE, OP_ALPHABETA]
LOG_PARAMS = [EVAL_STRING.replace(":", ""), DEPTH_STRING.replace(":", ""), FEN_STRING.replace(":", ""), ENGINE_STRING.replace(":", ""),
              MOVE_STRING.replace(":", ""), COLOR_STRING.replace(":", ""), ALPHA_BETA_BREAK_STRING.replace(":", ""),
              MAX_DEPTH_STRING.replace(":", ""), EXTRA_DEPTH_STRING.replace(":", ""), CACHE_STRING.replace(":", ""), MAXIMIZE_STRING.replace(":", "")]
#
# Helper for Parameters in LOG-File
#
def get_header():
  header = "Timestamp;Type;Op;"
  for param in LOG_PARAMS:
    header += param + ";"
  return header + "\n"

def FEN_PARAM(fen):
    return FEN_STRING+fen+";"

def MOVE_PARAM(move):
    return MOVE_STRING+str(move)+";"

def ENGINE_PARAM(engine):
    return ENGINE_STRING+engine+";"

def EVAL_PARAM(eval):
    return EVAL_STRING+str(eval)+";"

def DEPTH_PARAM(depth):
    return DEPTH_STRING+str(depth)+";"

def MAXIMIZE_PARAM(maximize):
    return MAXIMIZE_STRING+str(maximize)+";"

def ALPHA_BETA_BREAK_PARAM(value):
    return ALPHA_BETA_BREAK_STRING+str(value)+";"

def COLOR_PARAM(color):
    if color == chess.WHITE:
        color_str = "White"
    elif color == chess.BLACK:
        color_str = "Black"
    else:
        color_str = ""
    return COLOR_STRING+color_str+";"

def CONFIG_LOG_ENTRY(start_pos, nnue_lib, max_depth, extra_depth, cache):
    return CONFIG_STRING + f"FEN: {start_pos};" f"NNUE_LIB: {nnue_lib};" + MAX_DEPTH_STRING + f"{max_depth};" \
        + EXTRA_DEPTH_STRING + f"{extra_depth};" + CACHE_STRING +f"{cache};"