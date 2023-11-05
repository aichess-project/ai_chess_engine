import chess, chess.polyglot
from collections import namedtuple
import typing

WCK_INDEX = 8*8*12
WCQ_INDEX = WCK_INDEX + 1
BCK_INDEX = WCQ_INDEX + 1
BCQ_INDEX = BCK_INDEX + 1
EP_INDEX = BCQ_INDEX + 1
TURN_INDEX = EP_INDEX + 8

PAWN = 1
ROOK = PAWN + 3

# Define a named tuple for the chessboard state
PieceMoveState = namedtuple("PieceMoveState", [
    "ep",
    "turn",
    "wck",
    "wcq",
    "bck",
    "bcq",
    "move_from",
    "move_to",
    "ep_move",
    "piece_moved",
    "piece_captured",
    "piece_promoted"
])

def get_square_piece_index(piece, color, square):
     piece_index = get_piece_index(piece, color)
     square_piece_index = 64 * piece_index + square
     if square_piece_index < 0 or square_piece_index >= len(chess.polyglot.POLYGLOT_RANDOM_ARRAY):
         exit()
     return square_piece_index

def get_piece_index(piece, color):
    return (piece-1) * 2 + int(color)

def get_ep_index(ep, turn):
    if turn == chess.BLACK:
          index = ep-chess.A3
    else:
          index = ep-chess.A6
    return index + EP_INDEX

def update_hash(hash, array_index):
    hash ^= chess.polyglot.POLYGLOT_RANDOM_ARRAY[array_index]
    return hash

def get_board_move_state(board, move):
    if board.is_en_passant(move):
        ep = True
    else:
        ep = False
    return PieceMoveState(ep=board.ep_square,
                            turn=board.turn,
                            wck=board.has_kingside_castling_rights(chess.WHITE),
                            wcq=board.has_queenside_castling_rights(chess.WHITE),
                            bck=board.has_kingside_castling_rights(chess.BLACK),
                            bcq=board.has_queenside_castling_rights(chess.BLACK),
                            move_from = move.from_square,
                            move_to = move.to_square,
                            piece_moved = board.piece_type_at(move.from_square),
                            ep_move = ep,
                            piece_captured = board.piece_type_at(move.to_square),
                            piece_promoted = move.promotion)

def hash_board(board) -> int:
        zobrist_hash = 0
        for color, squares in enumerate(board.occupied_co):
            for square in chess.scan_reversed(squares):
                index = get_square_piece_index(board.piece_type_at(square), color, square)
                zobrist_hash = update_hash(zobrist_hash, index)
        if board.turn:
            zobrist_hash = update_hash(zobrist_hash, TURN_INDEX)
        if board.has_kingside_castling_rights(chess.WHITE):
            zobrist_hash = update_hash(zobrist_hash, WCK_INDEX)
        if board.has_queenside_castling_rights(chess.WHITE):
            zobrist_hash = update_hash(zobrist_hash, WCQ_INDEX)
        if board.has_kingside_castling_rights(chess.BLACK):
            zobrist_hash = update_hash(zobrist_hash, BCK_INDEX)
        if board.has_queenside_castling_rights(chess.BLACK):
            zobrist_hash = update_hash(zobrist_hash, BCQ_INDEX)
        if board.ep_square:
            if board.turn == chess.BLACK:
            # a3 is Square 16
                index = board.ep_square-16
            else:
            # a6 is Square 40
                index = board.ep_square-40
            zobrist_hash ^= chess.polyglot.POLYGLOT_RANDOM_ARRAY[EP_INDEX + index]
        return zobrist_hash

def get_zobrist_hash(board):
    hash = hash_board(board)
    return hash

def execute_move_update_hash(old_hash, move, board):
    move = chess.Move.from_uci(move)
    old_board_move_state = get_board_move_state(board, move)
    board.push(move)
    return increment_hash(board, old_board_move_state, old_hash)

def increment_hash(board, old_board_move_state, old_hash):
    # Turn has changed
    new_hash = update_hash(old_hash, TURN_INDEX)
    # OLD EP must be deleted
    if old_board_move_state.ep is not None:
        ep_index = get_ep_index(old_board_move_state.ep, old_board_move_state.turn)
        new_hash = update_hash(new_hash, ep_index)
    # Check the new non Move State Variables
    if board.ep_square is not None:
        ep_index = get_ep_index(board.ep_square, board.turn)
        new_hash = update_hash(new_hash, ep_index)
    if old_board_move_state.wck != board.has_kingside_castling_rights(chess.WHITE):
        new_hash = update_hash(new_hash, WCQ_INDEX)
    if old_board_move_state.wcq != board.has_queenside_castling_rights(chess.WHITE):
        new_hash = update_hash(new_hash, WCK_INDEX)
    if old_board_move_state.bcq != board.has_queenside_castling_rights(chess.BLACK):
        new_hash = update_hash(new_hash, BCQ_INDEX)
    if old_board_move_state.bck != board.has_kingside_castling_rights(chess.BLACK):
        new_hash = update_hash(new_hash, BCK_INDEX)
    # Update according to move
    new_hash = update_hash_move(old_board_move_state, new_hash)
    return new_hash

def update_hash_move(state, hash):
    # Clear the old square
    from_index = get_square_piece_index(piece = state.piece_moved, color = state.turn, square = state.move_from)
    hash = update_hash(hash, from_index)

    # Set new square
    if state.piece_promoted is None:
        piece = state.piece_moved
    else:
        piece = state.piece_promoted
    to_index = get_square_piece_index(piece = piece, color = state.turn, square = state.move_to)
    hash = update_hash(hash, to_index)
    if state.piece_captured is not None:
        capture_index = get_square_piece_index(piece = state.piece_captured, color = not state.turn, square = state.move_to)
        hash = update_hash(hash, capture_index)
        
    if state.ep_move:
        if state.turn == chess.BLACK:
            enemy_pawn_square = state.move_to + 8
        else:
            enemy_pawn_square = state.move_to - 8
        capture_index = get_square_piece_index(piece = PAWN, color = not state.turn, square = enemy_pawn_square)
        hash = update_hash(hash, capture_index)
    # Check Castling
    castling = False
    if state.move_from == chess.E1 and state.move_to == chess.G1:
        castling = True
        from_sq = chess.H1
        to_sq = chess.F1
        color = chess.WHITE
    elif state.move_from == chess.E1 and state.move_to == chess.C1:
        castling = True
        from_sq = chess.A1
        to_sq = chess.D1
        color = chess.WHITE
    elif state.move_from == chess.E8 and state.move_to == chess.G8:
        castling = True
        from_sq = chess.H8
        to_sq = chess.F8
        color = chess.WHITE
    elif state.move_from == chess.E8 and state.move_to == chess.C8:
        castling = True
        from_sq = chess.A8
        to_sq = chess.D8
        color = chess.BLACK
    if castling:
        from_index = get_square_piece_index(ROOK, color, from_sq)
        hash = update_hash(hash, from_index)
        to_index = get_square_piece_index(ROOK, color, to_sq)
        hash = update_hash(hash, to_index)

    return hash
