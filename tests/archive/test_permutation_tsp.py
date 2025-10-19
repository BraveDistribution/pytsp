import numpy as np

from pytsp.permutations_tsp import permutations_tsp
from pytsp.utils import route_cost


def test_permutation_algorithm():
    graph = np.array([[0, 5, 2, 1, 1, 4],
                      [5, 0, 6, 2, 2, 5],
                      [2, 6, 0, 7, 4, 2],
                      [1, 2, 7, 0, 8, 4],
                      [1, 2, 4, 8, 0, 5],
                      [4, 5, 2, 4, 5, 0]])
    route = [0, 1, 2, 3, 4, 5]
    result = permutations_tsp(graph)
    print(result)
    assert route_cost(graph,route) > route_cost(graph,result)


def test_permutation_algorithm_2():
    graph = np.array([[0, 4, 3, 4, 5, 1, 2, 3, 4],
                       [4, 0, 1, 4, 3, 4, 6, 2, 1],
                       [3, 1, 0, 1, 4, 3, 2, 1, 9],
                       [4, 4, 1, 0, 4, 6, 1, 2, 3],
                       [5, 3, 4, 4, 0, 1, 2, 5, 3],
                       [1, 4, 3, 6, 1, 0, 2, 5, 3],
                       [2, 6, 2, 1, 2, 2, 0, 3, 5],
                       [3, 2, 1, 2, 5, 5, 3, 0, 9],
                       [4, 1, 9, 3, 3, 3, 5, 0, 0]
                       ])
    route = [0,1,2,3,4,5,6,7,8]
    result = permutations_tsp(graph)
    print(route_cost(graph, result))
    assert route_cost(graph, route) > route_cost(graph,result)
