from itertools import permutations
from pytsp.utils import route_cost

def permutations_tsp(graph):
    """
    Creates all permutations from the added graph check all the combinations and the route costs and then
    returns the best solution. BEWARE: this method is computationally expensive, therefore it shouldn't be run on over 12 nodes
    Args:
        graph: graph

    Returns:
        list of nodes []
    """
    route = range(0, len(graph))
    # generate all permutations
    all_routes = [list(i) for i in permutations(route)]
    # calculate all costs
    cost_all_routes = [route_cost(graph, i) for i in all_routes]
    # find the lowest cost
    best_route = all_routes[cost_all_routes.index(min(cost_all_routes))]
    return best_route
