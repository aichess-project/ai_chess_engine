import chess, chess.polyglot, csv, cityhash
from ctypes import *
from datetime import datetime, timedelta
from engine_libs.zobrist import ZobristHash

def get_fen_hash(fen_str):
        hash64 = cityhash.CityHash64(fen_str)
        hash16 = (hash64 & 0xFFFF)
        return hash16

def evaluation_fen_pos(nnue, fen_str, color):
      eval = nnue.nnue_evaluate_fen(bytes(fen_str, encoding='utf-8'))/200.08
      if color == chess.BLACK:
        eval = -eval
      return eval
    
def evaluate_position(nnue, board):
    if board.is_checkmate():
        return float("-inf") if board.turn == chess.WHITE else float("inf")
    elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves():
        return 0.0
    fen_str = board.fen()
    return evaluation_fen_pos(nnue, fen_str, board.turn)

def test_zobrist():

    net_filename = "/Users/littlecapa/GIT/python/chess_engines/NNUE/nn-04cf2b4ed1da.nnue"
    nnue = cdll.LoadLibrary("/Users/littlecapa/GIT/python/chess_engines/NNUE/libnnueprobe.so")
    nnue.nnue_init(net_filename.encode('utf-8'))
    zh = ZobristHash()

    fen_list = []
    board_list = []

    max = 150000
    nr = 0

    with open('./test_data/fen_eval.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fen = row['FEN']
            fen_list.append(fen)
            nr += 1
            if nr >= max:
                break

    for fen in fen_list:
        board_list.append(chess.Board(fen=fen))

    start_time = datetime.now()
    for board in board_list:
        zobrist_hash = chess.polyglot.zobrist_hash(board)
    
    current_time = datetime.now()
    duration = (current_time - start_time).total_seconds()

    print(f"Zobrist Result Size: {len(board_list)} Duration {duration} {duration / len(board_list)}")

    start_time = datetime.now()
    for board in board_list:
        zobrist_hash = zh.set_board(board)
    
    current_time = datetime.now()
    duration = (current_time - start_time).total_seconds()

    print(f"New Zobrist Result Size: {len(board_list)} Duration {duration} {duration / len(board_list)}")

    start_time = datetime.now()
    for board in board_list:
        zobrist_hash = zh.set_board(board, variant = 2)
    
    current_time = datetime.now()
    duration = (current_time - start_time).total_seconds()

    print(f"New Zobrist2 Result Size: {len(board_list)} Duration {duration} {duration / len(board_list)}")

    start_time = datetime.now()
    for board in board_list:
        fen = board.fen()
    
    current_time = datetime.now()
    duration = (current_time - start_time).total_seconds()

    print(f"FEN Generation Results: {len(board_list)} Duration {duration} {duration / len(board_list)}")

    start_time = datetime.now()
    for fen in fen_list:
        hash = get_fen_hash(fen)
    
    current_time = datetime.now()
    duration = (current_time - start_time).total_seconds()

    print(f"FEN CityHash Results: {len(fen_list)} Duration {duration} {duration / len(board_list)}")

    start_time = datetime.now()
    for board in board_list:
        eval = evaluate_position(nnue, board)
    
    current_time = datetime.now()
    duration = (current_time - start_time).total_seconds()

    print(f"Board Eval Results: {len(board_list)} Duration {duration} {duration / len(board_list)}")

if __name__ == "__main__":
    test_zobrist()