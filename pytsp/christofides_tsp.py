import numpy as np

from .utils.utils import minimal_spanning_tree


def christofides_tsp(graph):
    """
    Christofides TSP algorithm
    http://www.dtic.mil/dtic/tr/fulltext/u2/a025602.pdf
    Args:
        graph: 2d numpy array matrix

    Returns:
        TSP
    """

    mst = minimal_spanning_tree(graph, 'Prim')
    odd_degree_nodes = _get_odd_degree_vertices(mst)


def _get_odd_degree_vertices(graph):
    """
    Finds all the odd degree vertices in graph
    Args:
        graph: 2d np array as adj. matrix

    Returns:
    Set of vertices that have odd degree
    """
    odd_degree_vertices = set()
    for index, row in enumerate(graph):
        if len(np.nonzero(row)[0]) % 2 != 0:
            odd_degree_vertices.add(index)
    return odd_degree_vertices
