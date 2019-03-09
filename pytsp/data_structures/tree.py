import numpy as np

from typing import List, Any

from pytsp.data_structures.node import Node


class Tree:
    """ Tree used in the branch and bound process of TSP"""

    def __init__(self, graph_size):
        self.node_indexes = set((range(graph_size)))
        self.leafs: List[Node] = []
        self.best_solution_value = None

    def add_leaf(self, node):
        if self.leafs:
            for index, leaf in enumerate(self.leafs):
                if node.bound < leaf.bound:
                    self.leafs.insert(index, node)
                    return
            self.leafs.append(node)
        else:
            self.leafs.append(node)


    def get_leaf_with_lowest_bound(self):
        return self.leafs[0]

    def remove_leaf_from_list(self, node):
        self.leafs.remove(node)

    def set_solution(self, value):
        self.best_solution_value = value

    def optimized(self):
        if self.best_solution_value is None or self.best_solution_value > self.leafs[0].bound:
            return False
        else:
            return True
