import logging
import numpy as np

from pytsp.data_structures.node import Node
from pytsp.data_structures.tree import Tree

logging.getLogger().setLevel(logging.DEBUG)

# TODO: Need to finish this on 1961 paper.


# hacky way to do it
INFINITY = 10000000


def branch_and_bound_tsp(graph):
    """
    2d numpy array, be cautious, it is cpu/memory/time expensive. Works on the asymetric tsp as well.
    :param graph:
    :return: exact solution
    """
    bnb_tree = Tree()

    # we create new distance matrix from reduced one
    new_graph, bound = reduce_graph(graph)

    first_node = Node(bound, None, new_graph)
    bnb_tree.add_leaf(first_node)

    if not bnb_tree.is_optimized():
        _optimize(bnb_tree)
    else:
        # construct path
        pass


def _optimize(bnb_tree: Tree):
    node: Node = bnb_tree.get_leaf_with_lower_bound()
    # remove node from list of leafs, because it has the children now

    bnb_tree.remove_leaf(node)

    left_node, right_node = _branch_and_get_children(node)


def reduce_graph(graph):
    """Reduces the matrix so at least one zero is in each column & each row"""
    lower_bound_reduction = 0
    matrix_size = len(graph)
    new_graph = graph.copy()

    for index in range(matrix_size):
        if 0 not in graph[index, :]:
            arr_min = min(graph[index, :])
            lower_bound_reduction += arr_min
            new_graph[index, :] = graph[index, :] - arr_min

    new_graph = new_graph.T
    for index in range(matrix_size):
        if 0 not in new_graph[index, :]:
            arr_min = min(new_graph[index, :])
            lower_bound_reduction += arr_min
            new_graph[index, :] = new_graph[index, :] - arr_min

    logging.debug("Lower bound reduction: %s" % lower_bound_reduction)
    return new_graph, lower_bound_reduction


def _calculate_delta_value(graph):
    """
    According to the original paper delta(k,l) = min of row K except K,L item +
    min of col L except K,L item

    We need to find the biggest delta and create a new branch. It is satisfactory to look only
    into 0 numbers in the array, because elsewhere it is still = 0.
    """

    row, col = np.where(graph == 0)
    delta_values = []
    for index_of_zero in range(len(row)):
        # minimum value of row + minimum value of column (excpt the row,col item
        delta_values.append(np.min(graph[row[index_of_zero], :][np.arange(len(graph)) != col[index_of_zero]]) +
                            np.min(graph[:, col[index_of_zero]][np.arange(len(graph)) != row[index_of_zero]]))

    biggest_delta_index = np.argmax(delta_values)
    return (row[biggest_delta_index], col[biggest_delta_index]), delta_values[biggest_delta_index]


def _branch_and_get_children(node: Node):
    """Branch and get the two children, set children of main node to the two"""
    row_col_tuple, delta_value = _calculate_delta_value(node.matrix)

    left_node = Node
    right_node = Node

    node.right_succ = right_node

    return Node, Node


def _branch_left(node: Node, row_col_tuple, delta_value):
    """Branch to left"""
    left_node = Node(delta_value, node, node.matrix)
    node.left_succ = left_node


def _branch_right(node: Node):
    """Branch to right"""
    submatrix = 0


def __remove_col_and_row_and_set_to_inf(matrix, row_col_tuple):
    """Create new submatrix with row/col crossed out and (row, col) set to 0"""
