import numpy as np

from pytsp.lin_kerdighan_tsp import _get_mst_and_add_two_edges, dad, get_B_matrix, _compute_degree_array, \
    _compute_lower_bound_w, _create_min_1_tree, subgradient_optimization


def test_get_mst_and_add_two_edges():
    test = np.array([
        [0, 2, 1, 3, 5],
        [2, 0, 10, 8, 7],
        [1, 10, 0, 3, 7],
        [3, 8, 3, 0, 4],
        [5, 7, 7, 4, 0],
    ])

    starting_node = 0
    result = _get_mst_and_add_two_edges(test, starting_node)

    test2 = np.array([[0, 2, 1, 0, 0],
                      [2, 0, 0, 0, 7],
                      [1, 0, 0, 3, 0],
                      [0, 0, 3, 0, 4],
                      [0, 7, 0, 4, 0]])

    np.testing.assert_array_equal(test2, result)


def test_dad_1():
    test = np.array([[0, 2, 1, 3, 0],
                     [2, 0, 0, 0, 0],
                     [1, 0, 0, 3, 0],
                     [3, 0, 3, 0, 4],
                     [0, 0, 0, 4, 0]])
    assert dad(test, 1) == 0
    assert dad(test, 2) == 0
    assert dad(test, 3) == 0


def test_B_matrix():
    graph = np.array([[0, 2, 1, 0, 0], [2, 0, 2, 2, 0], [1, 2, 0, 0, 3], [0, 2, 0, 0, 0], [0, 0, 3, 0, 0]])
    np.testing.assert_array_equal(get_B_matrix(graph), np.array(
        [[-10000, 0, 0, 0, 0], [0, -10000, 1, 2, 3], [0, 1, -10000, 2, 3], [0, 2, 2, -10000, 3],
         [0, 3, 3, 3, -10000]]))


def test_create_min_1_tree():
    graph = np.array([
        [0, 7, 0, 5, 0, 0, 0],
        [7, 0, 8, 9, 7, 0, 0],
        [0, 8, 0, 0, 5, 0, 0],
        [5, 9, 0, 0, 15, 6, 0],
        [0, 7, 5, 15, 0, 8, 9],
        [0, 0, 0, 6, 8, 0, 11],
        [0, 0, 0, 0, 9, 11, 0]
    ])

    result = np.array([
        [0, 7, 0, 5, 0, 0, 0],
        [7, 0, 0, 0, 7, 0, 0],
        [0, 0, 0, 0, 5, 0, 0],
        [5, 0, 0, 0, 0, 6, 0],
        [0, 7, 5, 0, 0, 0, 9],
        [0, 0, 0, 6, 0, 0, 11],
        [0, 0, 0, 0, 9, 11, 0]
    ])

    np.testing.assert_array_equal(_create_min_1_tree(graph), result)


def test_compute_degree_array():
    graph = np.array([[0, 2, 1, 0, 0], [2, 0, 2, 2, 0], [1, 2, 0, 0, 3], [0, 2, 0, 0, 0], [0, 0, 3, 0, 0]])
    result = np.array([2, 3, 3, 1, 1])
    np.testing.assert_array_equal(result, _compute_degree_array(graph))


def test_compute_lower_bound():
    pi_vector = np.array([1, 2, 3, 4, 5])
    min_1_tree = np.array([[0, 2, 1, 0, 0],
                           [2, 0, 0, 0, 7],
                           [1, 0, 0, 3, 0],
                           [0, 0, 3, 0, 4],
                           [0, 7, 0, 4, 0]])
    assert 4 == _compute_lower_bound_w(min_1_tree, pi_vector)


def test_subgradient_optimization():
    graph = np.array([
        [0, 7, 0, 5, 0, 0, 0],
        [7, 0, 8, 9, 7, 0, 0],
        [0, 8, 0, 0, 5, 0, 0],
        [5, 9, 0, 0, 15, 6, 0],
        [0, 7, 5, 15, 0, 8, 9],
        [0, 0, 0, 6, 8, 0, 11],
        [0, 0, 0, 0, 9, 11, 0]
    ])
    result = np.array([1, 1, 1, 1, 1, 1, 1])
    np.testing.assert_array_equal(result, subgradient_optimization(graph))
