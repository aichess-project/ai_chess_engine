class EvaluationCache:
    def __init__(self, cache_size, delete_rate):
        self.cache_size = cache_size
        self.cache = {}  # Use a dictionary for faster lookup
        self.delete_rate = delete_rate
        self.cache_length = 0
        self.nr_requests = 0
        self.nr_hits = 0
        self.nr_adds = 0

    def add_evaluation(self, fen_str, evaluation):
        if self.cache_length >= self.cache_size:
            # Remove a portion of the cache when it exceeds the size
            keys_to_remove = list(self.cache.keys())[:int(self.cache_size * self.delete_rate)]
            for key in keys_to_remove:
                del self.cache[key]
            self.cache_length = len(self.cache)
        self.cache[fen_str] = evaluation
        self.cache_length += 1
        self.nr_adds += 1

    def get_evaluation(self, fen_str):
        self.nr_requests += 1
        if fen_str in self.cache:
            self.nr_hits += 1
            return self.cache[fen_str]  # Return the evaluation
        return None

    def __del__(self):
        print(f"Add: {self.nr_adds} Requests: {self.nr_requests} Hits: {self.nr_hits}")