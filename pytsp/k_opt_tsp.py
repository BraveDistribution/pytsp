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
    """
    improved = True
    best_found_route = route
    best_found_route_cost = route_cost(graph, best_found_route)
    while improved:
        improved = False
        for i in range(len(best_found_route) - 1):
            for k in range(i + 1, len(best_found_route)):
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

