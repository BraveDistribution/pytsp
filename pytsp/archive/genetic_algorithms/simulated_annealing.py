from itertools import cycle, dropwhile, islice

import numpy as np
import random

from pytsp.constants import Constants
from pytsp.christofides_tsp import christofides_tsp
from pytsp.utils import route_cost

graph = np.array([[0, 4, 3, 4, 5, 1, 2, 3, 4],
                       [4, 0, 1, 4, 3, 4, 6, 2, 1],
                       [3, 1, 0, 1, 4, 3, 2, 1, 9],
                       [4, 4, 1, 0, 4, 6, 1, 2, 3],
                       [5, 3, 4, 4, 0, 1, 2, 5, 3],
                       [1, 4, 3, 6, 1, 0, 2, 5, 3],
                       [2, 6, 2, 1, 2, 2, 0, 3, 5],
                       [3, 2, 1, 2, 5, 5, 3, 0, 9],
                       [4, 1, 9, 3, 3, 3, 5, 9, 0]
                       ])


def simulated_annealing(graph, path=None, temperature=1, n_of_iter=1000, alpha=0.95):
    if path is None:
        path = christofides_tsp(graph)

    changed = True

    while changed:
        temp_solution = [node for node in path]
        for iter in range(n_of_iter):
            new_solution = _get_next_solution(path)

            new_route_cost = route_cost(graph, new_solution)
            current_route_cost = route_cost(graph, path)
            if new_route_cost < current_route_cost:
                path = new_solution
            else:
                if np.exp(
                    (current_route_cost - new_route_cost) / (temperature * Constants.BOLTZMANN)) > random.random():
                    path = new_solution

        temperature = _decrease_temperature(temperature, alpha)

        if temp_solution == path:
            changed = False

    # just to start with the same node -> we will need to cycle the results.
    cycled = cycle(path)
    skipped = dropwhile(lambda x: x != 0, cycled)
    sliced = islice(skipped, None, len(path))
    path = list(sliced)

    return path


def _get_next_solution(path):
    new_solution = [node for node in path]
    left_index = random.randint(2, len(path) - 1)
    right_index = random.randint(0, len(path) - left_index)
    new_solution[right_index: (right_index + left_index)] = reversed(
        new_solution[right_index: (right_index + left_index)])
    return new_solution


def _decrease_temperature(temperature, alfa):
    return alfa * temperature
