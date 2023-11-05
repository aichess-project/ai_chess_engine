from engine_libs.zobrist_hash import ZobristHash
from engine_libs.stack import Stack
from collections import namedtuple
import chess


class EvaluationHashCache:

    MY_PRIME = 11111
    MAX_GET_NEXT = 1

    StackItem = namedtuple("StackItem", [
        "board_move_state",
        "hash_value",
        "depth"
    ])

    CacheItem = namedtuple("CacheItem", [
        "board_hash",
        "fen_string",
        "eval",
        "depth"
    ])

    def get_stack_item(self, board_move_state, hash_value = None, depth = None):
        return EvaluationHashCache.StackItem(board_move_state = board_move_state, hash_value = hash_value, depth = depth)
    
    def get_cache_item(self, board_hash, fen_string, eval, depth):
        return EvaluationHashCache.CacheItem(board_hash = board_hash, fen_string = fen_string, eval = eval, depth = depth)

    def __init__(self, nnue, cache_size = 64000):
        self.cache_size = cache_size
        self.cache = [None]*self.cache_size
        self.nr_requests = 0
        self.nr_hits = 0
        self.nr_adds = 0
        self.nr_collisions = 0
        self.max_collisions = 0
        self.zh = ZobristHash()
        self.eval_stack = Stack()
        self.nnue = nnue

    def get_hash_key(self, hash_value):
        return hash_value % self.cache_size

    def set_board(self, board):
        hash_value = self.zh.get_zobrist_hash(board)
        self.board = board
        self.eval_stack.push(self.get_stack_item(board_move_state = None, hash_value=hash_value, depth = None))

    def make_move(self, move, depth):
        old_hash = self.eval_stack.top().hash_value
        #move = chess.Move.from_uci(move)
        state = self.zh.get_board_move_state(self.board, move)
        self.board.push(move)
        new_hash = self.zh.increment_hash(self.board, state, old_hash)
        self.eval_stack.push(self.get_stack_item(board_move_state = None, hash_value=new_hash, depth = depth))

    def take_move_back(self):
        self.eval_stack.pop()
        self.board.pop()

    def get_next_hash(self, hash):
        return (hash + EvaluationHashCache.MY_PRIME) % self.cache_size

    def add_evaluation(self, cache_item):
        #
        # Check for Collisions
        #
        cache_key = self.get_hash_key(cache_item.board_hash)
        counter = 0
        while self.cache[cache_key] is not None and counter < EvaluationHashCache.MAX_GET_NEXT:
            if self.cache[cache_key].board_hash == cache_item.board_hash and self.cache[cache_key].depth >= cache_item.depth:
                break
            counter += 1
        self.max_collisions = max(self.max_collisions, counter)
        self.cache[cache_key] = cache_item
        self.nr_adds += 1

    def evaluation_fen_pos(self, fen_str, color):
      eval = self.nnue.nnue_evaluate_fen(bytes(fen_str, encoding='utf-8'))/200.08
      if color == chess.BLACK:
        eval = -eval
      return eval
    
    def get_evaluation(self, depth):
        board_hash = self.eval_stack.top().hash_value
        self.nr_requests += 1
        cache_key = self.get_hash_key(board_hash)
        counter = 0
        while self.cache[cache_key] is not None and counter < EvaluationHashCache.MAX_GET_NEXT:
            cached_board_hash= self.cache[cache_key].board_hash
            cached_depth = self.cache[cache_key].depth
            if cached_board_hash != board_hash or cached_depth > depth:
                self.nr_collisions += 1
                cache_key = self.get_next_hash(cache_key)
                counter += 1
                self.max_collisions = max(self.max_collisions, counter)
            else:
                self.nr_hits += 1
                return self.cache[cache_key].eval
        fen_str = self.board.fen()
        eval = self.evaluation_fen_pos(fen_str, self.board.turn)
        self.add_evaluation(self.get_cache_item(board_hash, fen_str, eval, depth))
        return eval
    
    def __del__(self):
        counter = 0
        for i in range(self.cache_size):
            if self.cache[i] is not None:
                counter += 1
        print(f"Add: {self.nr_adds} Requests: {self.nr_requests} Hits: {self.nr_hits} Collisions: {self.nr_collisions} Max Collisions: {self.max_collisions} Counter: {counter}")