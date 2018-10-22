import numpy as np

from pytsp.christofides_tsp import _get_odd_degree_vertices


def test_get_odd_degree_vertices():
    graph = np.array([
        [0, 1, 3, 0, 2, 4],
        [0, 0, 4, 5, 6, 1],
        [2, 0, 0, 1, 2, 3],
        [3, 3, 1, 0, 3, 6],
        [0, 0, 0, 0, 1, 0]
    ])

    result = _get_odd_degree_vertices(graph)
    odd_degrees = {3, 4}

    assert result == odd_degrees
