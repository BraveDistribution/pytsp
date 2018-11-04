import numpy as np


from pytsp.lin_kerdighan_tsp import _get_mst_and_add_two_edges


def test_get_mst_and_add_two_edges():
    test = np.array([
        [0, 2, 1, 3, 5],
        [2, 0, 10, 8, 7],
        [1, 10, 0, 3, 7],
        [3, 8, 3, 0, 4],
        [5, 7, 7, 4, 0],
    ])

    starting_node = 2
    result = _get_mst_and_add_two_edges(test, starting_node)

    test2 = np.array([[0, 2, 1, 3, 0],
                      [2, 0, 0, 0, 0],
                      [1, 0, 0, 3, 0],
                      [3, 0, 3, 0, 4],
                      [0, 0, 0, 4, 0]])

    np.testing.assert_array_equal(test2, result)

