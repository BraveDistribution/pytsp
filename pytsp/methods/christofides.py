from time import time
from .utils import Instance, SolutionMethod, Tour
from networkx.algorithms.approximation import christofides

class Christofidesx(SolutionMethod):

    def __init__(self):

        self.name = "Christofides (networkx)"

    def solve(self, instance: Instance) -> Tour:
        """
        Solve a TSP instance using the Christofides heuristic.

        Returns:
            Tour: A Tour object containing the computed sequence and metadata.
        """
        try:
            # Start timing the algorithm
            start_time = time()

            # Create networkx graph (directly via TSPLIB)
            graph = instance.TSPLIB.get_graph()

            # Solve via christofides (from networkx)
            sequence = christofides(G=graph)

            # Create and return the final tour object
            tour = Tour(
                instance=instance,
                solution_method=self,
                sequence=sequence,
                runtime_in_sec=time() - start_time
            )

            return tour
        
        except Exception as error:
            print(f"An error occurred while solving {instance.name} with {self.name}: {error}")