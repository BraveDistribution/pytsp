import numpy as np

from pytsp.utils import minimal_spanning_tree


def lin_kerdighan_tsp(graph, starting_tour='', starting_node=0):
    """
    Lin-Kerdighan TSP: https://en.wikipedia.org/wiki/Lin–Kernighan_heuristic
    Args:
        graph: 2d numpy array matrix (undirected, weighted graph)
        starting_tour: type of starting tour

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
    result = np.insert(np.insert(mst_without_starting_node, 2, np.array([0, 0, 0, 0]), axis=0), 2,
                       np.array([0, 0, 0, 0, 0]), axis=1)
    result[starting_node][two_closest_edges[0]] = graph[starting_node][two_closest_edges[0]]
    result[starting_node][two_closest_edges[1]] = graph[starting_node][two_closest_edges[1]]

    result[two_closest_edges[0]][starting_node] = graph[starting_node][two_closest_edges[0]]
    result[two_closest_edges[1]][starting_node] = graph[starting_node][two_closest_edges[1]]
    return result
