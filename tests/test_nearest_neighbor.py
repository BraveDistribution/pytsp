import numpy as np

from pytsp.nearest_neighbor_tsp import nearest_neighbor_tsp


def test_nearest_neighbor():
    graph = np.array([[0, 300, 250, 190, 230],
                      [300, 0, 230, 330, 150],
                      [250, 230, 0, 240, 120],
                      [190, 330, 240, 0, 220],
                      [230, 150, 120, 220, 0]])
    result = [0, 3, 4, 2, 1]
    assert result == nearest_neighbor_tsp(graph)
