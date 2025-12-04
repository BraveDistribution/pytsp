class Node():
    """ One characterizing one subset in the branch and bound algorithm"""

    def __init__(self, bound, visited_nodes, predecessor):
        self.bound = bound
        self.visited_nodes = visited_nodes
        self.predecessor = predecessor

