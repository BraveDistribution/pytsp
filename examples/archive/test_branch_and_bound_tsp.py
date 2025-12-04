import numpy as np
from branch_and_bound_tsp_dfs import branch_and_bound_tsp_bfs

from pytsp.branch_and_bound_tsp import branch_and_bound_tsp, _calculate_delta_value, reduce_graph

np.set_printoptions(suppress=True)
INF = 100000


def test_bnb_function():
    graph = np.array([
        [INF, 27, 43, 16, 30, 26],
        [7, INF, 16, 1, 30, 25],
        [20, 13, INF, 35, 5, 0],
        [21, 16, 25, INF, 18, 18],
        [12, 46, 27, 48, INF, 5],
        [25, 5, 5, 9, 5, INF]
    ])

    path = branch_and_bound_tsp(graph)


def test_reduce_graph():
    graph = np.array([
        [INF, 27, 43, 16, 30, 26],
        [7, INF, 16, 1, 30, 25],
        [20, 13, INF, 35, 5, 0],
        [21, 16, 25, INF, 18, 18],
        [12, 46, 27, 48, INF, 5],
        [23, 5, 5, 9, 5, INF]
    ])

    reduced_matrix, lower_bound = reduce_graph(graph)
    print(lower_bound)
    pass


def test_get_delta_values():
    graph = np.array([
        [INF, 11, 27, 0, 14, 10],
        [1, INF, 15, 0, 29, 24],
        [15, 13, INF, 35, 5, 0],
        [0, 0, 9, INF, 2, 2],
        [2, 41, 22, 43, INF, 0],
        [13, 0, 0, 4, 0, INF]
    ])

    print(_calculate_delta_value(graph))


def test_bnb_dfs():
    test = np.array([
        [0, 2, 4, 5, 1],
        [2, 0, 5, 9, 2],
        [4, 5, 0, 1, 3],
        [5, 9, 1, 0, 2],
        [1, 2, 3, 2, 0]
    ])

    branch_and_bound_tsp_bfs(test)
