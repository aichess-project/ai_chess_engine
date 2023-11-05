from engine_libs.eval_cache_dict import EvaluationCache
def test_evaluation_cache():
    # Create an EvaluationCache with a size of 5 and a cache_move_length of 3
    cache = EvaluationCache(cache_size=5, delete_rate = 0.4)

    # Add evaluations to the cache
    cache.add_evaluation("fen1", 0.1)
    cache.add_evaluation("fen2", 0.2)
    cache.add_evaluation("fen3", 0.3)
    cache.add_evaluation("fen4", 0.4)
    cache.add_evaluation("fen5", 0.5)

    #cache.dump()

    assert cache.get_evaluation("fen1") == 0.1
    assert cache.get_evaluation("fen2") == 0.2
    assert cache.get_evaluation("fen3") == 0.3
    assert cache.get_evaluation("fen4") == 0.4
    assert cache.get_evaluation("fen5") == 0.5

    cache.add_evaluation("fen6", 0.6)
    assert cache.get_evaluation("fen1") == None
    assert cache.get_evaluation("fen2") == None
    assert cache.get_evaluation("fen3") == 0.3
    assert cache.get_evaluation("fen6") == 0.6
    assert cache.get_evaluation("xxx") == None

    
if __name__ == "__main__":
    test_evaluation_cache()
    print("All tests passed.")
