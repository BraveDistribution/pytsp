import numpy as np

from pytsp.constants import Constants


def nearest_neighbor_tsp(graph, starting_point=0):
    """
    Nearest neighbor TSP algorithm
    Args:
        graph: 2d numpy array
        starting_point: index of starting node

    Returns:
        tour approximated by nearest neighbor tsp algorithm
    Examples:
        >>> import numpy as np
        >>> graph = np.array([[  0, 300, 250, 190, 230],
        >>>                   [300,   0, 230, 330, 150],
        >>>                   [250, 230,   0, 240, 120],
        >>>                   [190, 330, 240,   0, 220],
        >>>                   [230, 150, 120, 220,   0]])
        >>> nearest_neighbor_tsp(graph)
    """
    number_of_nodes = len(graph)
    unvisited_nodes = list(range(number_of_nodes))
    unvisited_nodes.remove(starting_point)
    visited_nodes = [starting_point]

    while number_of_nodes > len(visited_nodes):
        neighbors = _find_neighbors(
            np.array(graph[visited_nodes[-1]]))

        not_visited_neighbours = list(
            set(neighbors[0].flatten()).intersection(unvisited_nodes))

        # pick the one travelling salesman has not been to yet
        try:
            next_node = _find_next_pickup_item(
                not_visited_neighbours, np.array(graph[visited_nodes[-1]]))
        except ValueError:
            print("Nearest Neighbor algorithm couldn't find a neighbor that hasn't been to yet")
            return
        visited_nodes.append(next_node)
        unvisited_nodes.remove(next_node)
    return visited_nodes


def _find_neighbors(array_of_edges_from_node):
    """
        Find the list of all neighbors for given node from adjacency matrix.
        Args:
            array_of_edges_from_node (np.array):

        Returns:
            List [] of all neighbors for given node
        """
    mask = (array_of_edges_from_node > 0) & (
        array_of_edges_from_node < Constants.MAX_WEIGHT_OF_EDGE)
    return np.where(np.squeeze(np.asarray(mask)))


def _find_next_pickup_item(not_visited_neighbors, array_of_edges_from_node):
    """

    Args:
        not_visited_neighbors:
        array_of_edges_from_node:

    Returns:

    """
    # last node in visited_nodes is where the traveling salesman is.
    cheapest_path = np.argmin(
        array_of_edges_from_node[not_visited_neighbors])
    return not_visited_neighbors[cheapest_path]
