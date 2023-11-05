import chess, chess.polyglot, csv
from datetime import datetime, timedelta
from engine_libs.zobrist_hash import ZobristHash


def test_zobrist():

    fen_list = []
    board_list = []

    max = 150000
    max = 10
    nr = 0

    zh = ZobristHash()

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
    #for board in board_list:
    #    zobrist_hash, board_state = get_zobrist_board(board)
    
    current_time = datetime.now()
    duration = (current_time - start_time).total_seconds()

    print(f"Zobrist Result Size: {len(board_list)} Duration {duration} {duration / len(board_list)}")

    board = chess.Board()
    moves_to_execute = ["e2e4", "e7e5", "g1f3", "b8c6", "f3e5","d7d5", "c2c4", "e8e7", "f1e2", "d5c4", "e1g1", "e7e8", "b2b4", "c4b3", "a2b3"]

    print("Start Test1")
    zobrist_hash = zh.get_zobrist_hash(board)
    for move in moves_to_execute:
        zobrist_hash = zh.execute_move_update_hash(zobrist_hash, move, board)
        expected_hash = zh.get_zobrist_hash(board)
        print (move, zobrist_hash, expected_hash, zobrist_hash == expected_hash)
        assert zobrist_hash == expected_hash
        zobrist_hash = expected_hash

    board = chess.Board()
    moves_to_execute = ["h2h3", "g7g6", "b2b3", "b7b6", "c1b2","c8b7", "b2h8", "b7g2"]

    print("Start Test2")
    zobrist_hash = zh.get_zobrist_hash(board)
    for move in moves_to_execute:
        zobrist_hash = zh.execute_move_update_hash(zobrist_hash, move, board)
        expected_hash = zh.get_zobrist_hash(board)
        print (move, zobrist_hash, expected_hash, zobrist_hash == expected_hash)
        assert zobrist_hash == expected_hash
        zobrist_hash = expected_hash

    print("Start Test3")
    board = chess.Board()
    zobrist_hash = zh.get_zobrist_hash(board)
    moves_to_execute = ["e2e3", "e7e6", "e1e2", "d7d5", "h2h4", "a7a5", "h4h5", "a5a4", "h5h6","a4a3", "h6g7", "a3b2", "g7h8q", "b2c1n"]
    for move in moves_to_execute:
        zobrist_hash = zh.execute_move_update_hash(zobrist_hash, move, board)
        expected_hash = zh.get_zobrist_hash(board)
        print (move, zobrist_hash, expected_hash, zobrist_hash == expected_hash)
        assert zobrist_hash == expected_hash
        zobrist_hash = expected_hash

    print("New Test")
    board = chess.Board()
    zobrist_hash = zh.get_zobrist_hash(board)
    moves_to_execute = ["h2h4", "e7e5", "h4h5", "f8e7", "h5h6","g8f6", "h6g7", "h7h5", "g7g8q"]
    for move in moves_to_execute:
        zobrist_hash = zh.execute_move_update_hash(zobrist_hash, move, board)
        expected_hash = zh.get_zobrist_hash(board)
        print (move, zobrist_hash, expected_hash, zobrist_hash == expected_hash)
        assert zobrist_hash == expected_hash
        zobrist_hash = expected_hash

if __name__ == "__main__":
    test_zobrist()