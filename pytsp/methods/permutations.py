from time import time
from .utils import Instance, SolutionMethod, Tour, get_sequence_weight
from itertools import permutations
from math import factorial

class Permutations(SolutionMethod):
    """
    Authors: Matej Gazda (gazda.matej@gmail.com), Arne Heinold (arne.heinold@klu.org)
    """

    def __init__(self, logging_level: int = 30):
        """
        Initialize the permutation (brute force) approach.

        Args:
            logging_level (int): Controls verbosity of output. Levels: NOTSET(0), DEBUG(10), INFO(20), WARNING(30), ERROR(40), CRITICAL(50)
        """

        # Initialize core attributes for the solution method
        super().__init__(name="Permutations", 
                         info=None, 
                         logging_level=logging_level)


    def solve(self, instance: Instance, max_nodes=10) -> Tour:
        """
        Solve a TSP instance by checking all permutations from the added instance. 
        This method is computationally expensive and shouldn't be run for instances with more than 12 nodes.
        Symmetric duplicates are not elimanted. For example, [1, 2, 3, 4, 1] and [1, 4, 3, 2, 1] are distinct.

        Args:
            instance (Instance): An instance of the TSP instance class.
            max_nodes (int, optional): Limit the number of nodes considered.

        Returns:
            Tour: A Tour object containing the computed sequence and metadata.
        """

        # Start timing the algorithm
        start_time = time()

        # Apply max_nodes limit if set
        nodes = instance.nodes[:max_nodes] if max_nodes else instance.nodes
        self.logger.info(f"Node list truncated to first {max_nodes} nodes out of {len(instance.nodes)} nodes.")

        # Estimate number of tours
        num_tours = factorial(len(nodes) - 1)
        self.logger.warning(f"Generating {num_tours} possible tours... This may take some time.")

        # Fix the starting node
        start = nodes[0]
        rest = nodes[1:]

        # Generate all possible tours
        sequences = []
        for perm in permutations(rest):
            sequence = [start] + list(perm) + [start]
            sequences.append(sequence)

        # Find the tour with the lowest weight
        best_sequence = min(
            sequences,
            key=lambda sequence: get_sequence_weight(instance=instance, sequence=sequence)
        )

        # Create and return the final tour object
        tour = Tour(
            instance=instance,
            solution_method=self,
            sequence=best_sequence,
            runtime_in_sec=time() - start_time
        )

        return tour
