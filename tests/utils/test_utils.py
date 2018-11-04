import numpy as np

from numpy.testing import assert_array_equal
from pytsp.utils import minimal_spanning_tree


def test_prim_algorithm():
    starting_node = 3
    graph = np.array([
        [0, 7, 0, 5, 0, 0, 0],
        [7, 0, 8, 9, 7, 0, 0],
        [0, 8, 0, 0, 5, 0, 0],
        [5, 9, 0, 0, 15, 6, 0],
        [0, 7, 5, 15, 0, 8, 9],
        [0, 0, 0, 6, 8, 0, 11],
        [0, 0, 0, 0, 9, 11, 0]
    ])

    min_spanning_tree = minimal_spanning_tree(graph, mode='Prim', starting_node=starting_node)

    result = np.array([
        [0, 7, 0, 5, 0, 0, 0],
        [7, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 5, 0, 0],
        [5, 0, 0, 0, 0, 6, 0],
        [0, 7, 5, 0, 0, 0, 9],
        [0, 0, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 9, 0, 0]
    ])

    assert_array_equal(result, min_spanning_tree)


def test_prim_algo2():
    test = np.array([
        [0, 2, 3, 5],
        [2, 0, 8, 7],
        [3, 8, 0, 4],
        [5, 7, 4, 0],
    ])
    min_spanning_tree = minimal_spanning_tree(test)
    print(min_spanning_tree)
