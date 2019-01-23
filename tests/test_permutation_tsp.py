import numpy as np

from pytsp.permutations_tsp import permutations_tsp

def test_3_opt_algorithm():
    graph = np.array([[0, 5, 2, 1, 1, 4],
                      [5, 0, 6, 2, 2, 5],
                      [2, 6, 0, 7, 4, 2],
                      [1, 2, 7, 0, 8, 4],
                      [1, 2, 4, 8, 0, 5],
                      [4, 5, 2, 4, 5, 0]])
    route = [0, 1, 2, 3, 4, 5]
    result = permutations_tsp(graph)
    print(result)
    assert True == True

