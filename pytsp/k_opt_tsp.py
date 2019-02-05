from itertools import cycle, islice, dropwhile

from pytsp.christofides_tsp import christofides_tsp
from pytsp.data_structures.opt_case import OptCase
from pytsp.utils import route_cost


def _swap_2opt(route, i, k):
    """ Swapping the route """
    new_route = route[0:i]
    new_route.extend(reversed(route[i:k + 1]))
    new_route.extend(route[k + 1:])
    return new_route


def tsp_2_opt(graph, route):
    """
    Approximate the optimal path of travelling salesman according to 2-opt algorithm
    Args:
        graph: 2d numpy array as graph
        route: list of nodes

    Returns:
        optimal path according to 2-opt algorithm

    Examples:
        >>> import numpy as np
        >>> graph = np.array([[  0, 300, 250, 190, 230],
        >>>                   [300,   0, 230, 330, 150],
        >>>                   [250, 230,   0, 240, 120],
        >>>                   [190, 330, 240,   0, 220],
        >>>                   [230, 150, 120, 220,   0]])
        >>> tsp_2_opt(graph)
    """
    improved = True
    best_found_route = route
    best_found_route_cost = route_cost(graph, best_found_route)
    while improved:
        improved = False
        for i in range(1, len(best_found_route) - 1):
            for k in range(i + 1, len(best_found_route) - 1):
                new_route = _swap_2opt(best_found_route, i, k)
                new_route_cost = route_cost(graph, new_route)
                if new_route_cost < best_found_route_cost:
                    best_found_route_cost = new_route_cost
                    best_found_route = new_route
                    improved = True
                    break
            if improved:
                break
    return best_found_route


def tsp_3_opt(graph, route=None):
    """
    Approximate the optimal path of travelling salesman according to 3-opt algorithm
    Args:
        graph:  2d numpy array as graph
        route: route as ordered list of visited nodes. if no route is given, christofides algorithm is used to create one.

    Returns:
        optimal path according to 3-opt algorithm
    Examples:
        >>> import numpy as np
        >>> graph = np.array([[  0, 300, 250, 190, 230],
        >>>                   [300,   0, 230, 330, 150],
        >>>                   [250, 230,   0, 240, 120],
        >>>                   [190, 330, 240,   0, 220],
        >>>                   [230, 150, 120, 220,   0]])
        >>> tsp_3_opt(graph)
    """
    if route is None:
        route = christofides_tsp(graph)
    moves_cost = {OptCase.opt_case_1: 0, OptCase.opt_case_2: 0,
                  OptCase.opt_case_3: 0, OptCase.opt_case_4: 0, OptCase.opt_case_5: 0,
                  OptCase.opt_case_6: 0, OptCase.opt_case_7: 0, OptCase.opt_case_8: 0}
    improved = True
    best_found_route = route
    while improved:
        improved = False
        for (i, j, k) in possible_segments(len(graph)):
            # we check all the possible moves and save the result into the dict
            for opt_case in OptCase:
                moves_cost[opt_case] = get_solution_cost_change(graph, best_found_route, opt_case, i, j, k)
            # we need the minimum value of substraction of old route - new route
            best_return = max(moves_cost, key=moves_cost.get)
            if moves_cost[best_return] > 0:
                best_found_route = reverse_segments(best_found_route, best_return, i, j, k)
                improved = True
                break
    # just to start with the same node -> we will need to cycle the results.
    cycled = cycle(best_found_route)
    skipped = dropwhile(lambda x: x != 0, cycled)
    sliced = islice(skipped, None, len(best_found_route))
    best_found_route = list(sliced)
    return best_found_route


def possible_segments(N):
    """ Generate the combination of segments """
    segments = ((i, j, k) for i in range(N) for j in range(i + 2, N-1) for k in range(j + 2, N - 1 + (i > 0)))
    return segments


def get_solution_cost_change(graph, route, case, i, j, k):
    """ Compare current solution with 7 possible 3-opt moves"""
    A, B, C, D, E, F = route[i - 1], route[i], route[j - 1], route[j], route[k - 1], route[k % len(route)]
    if case == OptCase.opt_case_1:
        # first case is the current solution ABC
        return 0
    elif case == OptCase.opt_case_2:
        # second case is the case A'BC
        return graph[A, B] + graph[E, F] - (graph[B, F] + graph[A, E])
    elif case == OptCase.opt_case_3:
        # ABC'
        return graph[C, D] + graph[E, F] - (graph[D, F] + graph[C, E])
    elif case == OptCase.opt_case_4:
        # A'BC'
        return graph[A, B] + graph[C, D] + graph[E, F] - (graph[A, D] + graph[B, F] + graph[E, C])
    elif case == OptCase.opt_case_5:
        # A'B'C
        return graph[A, B] + graph[C, D] + graph[E, F] - (graph[C, F] + graph[B, D] + graph[E, A])
    elif case == OptCase.opt_case_6:
        # AB'C
        return graph[B, A] + graph[D, C] - (graph[C, A] + graph[B, D])
    elif case == OptCase.opt_case_7:
        # AB'C'
        return graph[A, B] + graph[C, D] + graph[E, F] - (graph[B, E] + graph[D, F] + graph[C, A])
    elif case == OptCase.opt_case_8:
        # A'B'C
        return graph[A, B] + graph[C, D] + graph[E, F] - (graph[A, D] + graph[C, F] + graph[B, E])

def reverse_segments(route, case, i, j, k):
    """
    Create a new tour from the existing tour
    Args:
        route: existing tour
        case: which case of opt swaps should be used
        i:
        j:
        k:

    Returns:
        new route
    """
    if (i - 1) < (k % len(route)):
        first_segment = route[k% len(route):] + route[:i]
    else:
        first_segment = route[k % len(route):i]
    second_segment = route[i:j]
    third_segment = route[j:k]

    if case == OptCase.opt_case_1:
        # first case is the current solution ABC
        pass
    elif case == OptCase.opt_case_2:
        # A'BC
        solution = list(reversed(first_segment)) + second_segment + third_segment
    elif case == OptCase.opt_case_3:
        # ABC'
        solution = first_segment + second_segment + list(reversed(third_segment))
    elif case == OptCase.opt_case_4:
        # A'BC'
        solution = list(reversed(first_segment)) + second_segment + list(reversed(third_segment))
    elif case == OptCase.opt_case_5:
        # A'B'C
        solution = list(reversed(first_segment)) + list(reversed(second_segment)) + third_segment
    elif case == OptCase.opt_case_6:
        # AB'C
        solution = first_segment + list(reversed(second_segment)) + third_segment
    elif case == OptCase.opt_case_7:
        # AB'C'
        solution = first_segment + list(reversed(second_segment)) + list(reversed(third_segment))
    elif case == OptCase.opt_case_8:
        # A'B'C
        solution = list(reversed(first_segment)) + list(reversed(second_segment)) + list(reversed(third_segment))
    return solution
