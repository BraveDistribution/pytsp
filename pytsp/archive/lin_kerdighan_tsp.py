import numpy as np

from math import ceil, floor

from pytsp.utils import minimal_spanning_tree


def lin_kerdighan_tsp(graph, starting_tour='', starting_node=0):
    """
    Lin-Kerdighan TSP: https://en.wikipedia.org/wiki/Lin–Kernighan_heuristic
    Args:
        graph: 2d numpy array matrix (undirected, weighted graph)
        starting_tour: type of starting tour
        starting_node:

    Returns:
        TSP
    """

    if starting_tour == '':
        pass

    _get_mst_and_add_two_edges(graph, starting_node)


def _get_mst_and_add_two_edges(graph, starting_node):
    """
    We need to create MST from graph except the starting node. After the MST is created, we need to connect 2 closest edges
    with starting_node to create a cycle.
    Args:
        graph: 2d numpy array matrix
        starting_node: starting node

    Returns:
        MST with cycle at the start node

    // TODO maybe this one needs optimization, unfortunately I am not really high-efficient with numpy.
    """
    mst_without_starting_node = minimal_spanning_tree(
        np.delete(np.delete(graph, starting_node, axis=1), starting_node, axis=0), starting_node=starting_node)

    # 0 means that the edge does not exist
    two_closest_edges = np.argsort(np.ma.masked_equal(graph[starting_node], 0.0, copy=False))[:2]

    # we need to populate the result
    result = np.insert(np.insert(mst_without_starting_node, 0, np.array([0, 0, 0, 0]), axis=0), 0,
                       np.array([0, 0, 0, 0, 0]), axis=1)
    result[starting_node][two_closest_edges[0]] = graph[starting_node][two_closest_edges[0]]
    result[starting_node][two_closest_edges[1]] = graph[starting_node][two_closest_edges[1]]

    result[two_closest_edges[0]][starting_node] = graph[starting_node][two_closest_edges[0]]
    result[two_closest_edges[1]][starting_node] = graph[starting_node][two_closest_edges[1]]
    return result


def get_B_matrix(one_tree_graph):
    """ Calculate matrix of B values """
    B = np.zeros((len(one_tree_graph), len(one_tree_graph)))
    B[0][0] = -10000
    B[len(one_tree_graph) - 1][len(one_tree_graph) - 1] = -10000
    for i in range(1, len(one_tree_graph) - 1):
        B[i][i] = -10000
        for j in range(i + 1, len(one_tree_graph)):
            dad_node = dad(one_tree_graph, j)
            B[i][j] = max(B[i][j], one_tree_graph[j][dad_node])
            B[j][i] = B[i][j]
    return B


def dad(graph, node):
    """Calculate dad of the given node from np.array graph"""
    return np.where(graph[node] > 0)[0][0]


def create_D_matrix(cost_matrix, pi_vector_new):
    """
    According to the paper, transofrmation into the D matrix significantly improves the approximation.
    D[i][j] = cost_matrix[i][j] + pi[i]+pi[j], where pi is a vector.
    pi^(k+1) = pi^k + t^k*v^k

    The aim is now to find a transformation C->D, given by the vector pi = (pi1, pi2, ..., pin), that maximizes the lower bound
    w(pi)=L(Tn) - 2*sum(pii).
    Args:
        cost_matrix (2d np. array):

    Returns:
    Transformed cost matrix into D_matrix (2d np.array).
    """
    nodes_count = len(cost_matrix)
    for row in range(nodes_count):
        for col in range(nodes_count):
            cost_matrix[row][col] = cost_matrix[row][col] + pi_vector_new[row] + pi_vector_new[col]
    return cost_matrix


def _create_min_1_tree(matrix):
    """Create minimum 1 tree
    Special node for 1 tree computation is not fixed.
    Create MST and choose one leaf that has the longest second nearest neighbour distance
    """
    result = minimal_spanning_tree(matrix)
    matrix_without_mst = matrix - result
    min_values = list(map(lambda x: -1 if len(np.nonzero(x)[0]) == 0 else np.min(x[np.nonzero(x)]), matrix_without_mst))
    special_edge_start = np.argmax(min_values)
    special_edge_end = np.where(matrix_without_mst[special_edge_start] == min_values[special_edge_start])[0][0]
    result[special_edge_start][special_edge_end] = matrix[special_edge_start][special_edge_end]
    result[special_edge_end][special_edge_start] = matrix[special_edge_end][special_edge_start]
    return result


def subgradient_optimization(matrix):
    """
    Subgradient optimization of the given
    Args:
        matrix:
    Returns:
    """
    nodes_count = len(matrix)

    # initialize parameters
    pi_vector = np.zeros(nodes_count)
    W = -1000000

    # look at LKH report to understand this more clearly.
    period = ceil(nodes_count / 2)
    period_left = period
    step_size = 1
    D = matrix
    prev_subgradient_vector = 0
    W_prev = W
    for k in range(10000):
        # minimum 1 tree
        min_1_tree = _create_min_1_tree(D)

        # lower bound
        w_pi_k = _compute_lower_bound_w(min_1_tree, pi_vector)
        W = max(w_pi_k, W)

        subgradient_vector = _compute_degree_array(min_1_tree) - 2

        # Step size is doubled in the beginning of the first period until W does not increase
        if W > W_prev and k < period:
            step_size = step_size * 2

        # in the first iteration set  prev_subgradient_vector to v_k or else in the calculation pi vector it would fail
        if k is 0:
            prev_subgradient_vector = subgradient_vector

        pi_vector = pi_vector + step_size * (
            0.7 * subgradient_vector + 0.3 * prev_subgradient_vector)  # update pi vector

        # condition for termination
        if step_size is 0 or period is 0 or sum(subgradient_vector) is 0:
            break

        period_left = period_left - 1

        if period_left is 0:
            # if W was increased, then the period should be doubled.
            if W > W_prev:
                period = period * 2
                period_left = period
            else:
                period = floor(period / 2)
                period_left = period
            # step size is halved
            step_size = ceil(period / 2)

        prev_subgradient_vector = subgradient_vector
        W_prev = W

        D = create_D_matrix(matrix, pi_vector)

    return pi_vector


def _compute_lower_bound_w(min_1_tree: np.array, pi_vector: np.array) -> float:
    """
    Calculate the lower bound for given min-1-tree and vector pi
    Args:
        min_1_tree:
        pi_vector:

    Returns:
    lower_bound_w (float) = (length of min-1_tree - 2*sum of items in pi_vector).
    """
    return np.sum(min_1_tree) - 2 * np.sum(pi_vector)


def _compute_degree_array(min_1_tree):
    """Calculates the vector that saves the degree of nodes"""
    degree_vector_array = np.zeros(len(min_1_tree))
    for index, node in enumerate(min_1_tree):
        degree_vector_array[index] = np.count_nonzero(node)
    return degree_vector_array
