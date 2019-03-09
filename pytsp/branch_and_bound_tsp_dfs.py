import numpy as np

from numpy.core.multiarray import ndarray

from pytsp.data_structures.node import Node
from pytsp.data_structures.tree import Tree
from pytsp.utils import route_cost


def branch_and_bound_tsp_bfs(graph: ndarray):
    """ Branch and bound by BFS, lower bound is spanning tree"""
    number_of_nodes = len(graph)
    bnb_tree = Tree(number_of_nodes)

    # top level node
    top_lower_bound = 0
    for node in graph:
        top_lower_bound += np.sum(np.sort(node[node.nonzero()])[:2])

    # top node
    top_node = Node(top_lower_bound / 2, [0], graph)
    bnb_tree.add_leaf(top_node)

    while not bnb_tree.optimized():
        most_promising_leaf = bnb_tree.get_leaf_with_lowest_bound()
        bnb_tree.remove_leaf_from_list(most_promising_leaf)

        unvisited_nodes = list(bnb_tree.node_indexes - set(most_promising_leaf.visited_nodes))
        for vertex in unvisited_nodes:
            lower_bound = calculate_two_neighbor_bound(graph, most_promising_leaf, vertex)
            new_leaf = Node(lower_bound, most_promising_leaf.visited_nodes + [vertex], most_promising_leaf)
            bnb_tree.add_leaf(new_leaf)

            if len(new_leaf.visited_nodes) is number_of_nodes:
                new_leaf.visited_nodes.append(0)
                bnb_tree.set_solution(route_cost(graph, new_leaf.visited_nodes))
                print(*new_leaf.visited_nodes, sep=", ")
                print('Solution found %s' % (str(route_cost(graph, new_leaf.visited_nodes))))
                bnb_tree.remove_leaf_from_list(new_leaf)

    print('Best solution found: %s' % str(bnb_tree.best_solution_value))


def calculate_two_neighbor_bound(graph, predecessor, next_vertex_index):
    """Calculate two neighbor bound, it means take all nodes"""
    node_from = predecessor.visited_nodes[-1]
    node_to = next_vertex_index

    node_from_array = graph[node_from]
    node_to_array = graph[node_to]

    lower_bound = predecessor.bound - (
        np.min(node_from_array[node_from_array.nonzero()]) + np.min(node_to_array[node_to_array.nonzero()])) / 2 + \
                  graph[node_from][node_to]
    return lower_bound
