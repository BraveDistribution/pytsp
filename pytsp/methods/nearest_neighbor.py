from time import time
import numpy as np
from .utils import Instance, SolutionMethod, Tour

class NearestNeighbor(SolutionMethod):
    """
    Author: Arne Heinold (arne.heinold@klu.org)
    """

    def __init__(self, logging_level: int = 30):
        """
        Initialize the Nearest Neighbor heuristic.

        Args:
            logging_level (int): Controls verbosity of output. Levels: NOTSET(0), DEBUG(10), INFO(20), WARNING(30), ERROR(40), CRITICAL(50)
        """

        # Initialize core attributes for the solution method
        super().__init__(name="Nearest Neighbor", 
                         info=None, 
                         logging_level=logging_level)

    def solve(self, instance: Instance) -> Tour:
        """
        Solve a TSP instance using the Nearest Neighbor heuristic.
        
        Args:
            instance (Instance): An instance of the TSP instance class.

        Returns:
            Tour: A Tour object containing the computed sequence and metadata.
        """

        # Start timing the algorithm
        start_time = time()

        # Get number of stops and initial node sequence
        n = instance.number_of_stops
        sequence = instance.nodes.copy()

        # Iterate through each node in the sequence (except first and last)
        for i in range(1, n - 1):

            # Get the previous node
            x = sequence[i - 1]

            # Find the nearest neighbor among remaining nodes
            for j in range(i + 1, n):
                if instance.get_weight(source=x, target=sequence[j]) < instance.get_weight(source=x, target=sequence[i]):
                    # Swap current node with a closer one
                    sequence[i], sequence[j] = sequence[j], sequence[i]

        # Add return trip
        sequence.append(sequence[0])

        # Create and return the final tour object
        tour = Tour(
            instance=instance,
            solution_method=self,
            sequence=sequence,            
            runtime_in_sec=time() - start_time
        )

        return tour
