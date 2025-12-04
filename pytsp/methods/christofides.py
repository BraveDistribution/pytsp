from time import time
from .utils import Instance, SolutionMethod, Tour
from networkx.algorithms.approximation import christofides

class Christofidesx(SolutionMethod):
    """
    Author: Arne Heinold (arne.heinold@klu.org)
    """

    def __init__(self, logging_level: int = 30):
        """
        Initialize the Christofides heuristic.

        Args:
            logging_level (int): Controls verbosity of output. Levels: NOTSET(0), DEBUG(10), INFO(20), WARNING(30), ERROR(40), CRITICAL(50)
        """

        # Initialize core attributes for the solution method
        super().__init__(name="Christofides", 
                         info="Networkx implementation", 
                         logging_level=logging_level)

    def solve(self, instance: Instance) -> Tour:
        """
        Solve a TSP instance using the Christofides heuristic as implemented in networkx.

        Args:
            instance (Instance): An instance of the TSP instance class.

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

            # Covert to a sequence of node objects
            id_to_node = {n.id: n for n in instance.nodes}
            sequence = [id_to_node[n] for n in sequence]

            # Create and return the final tour object
            tour = Tour(
                instance=instance,
                solution_method=self,
                sequence=sequence,
                runtime_in_sec=time() - start_time
            )

            return tour
        
        except Exception as error:
            self.logger.error(f"An error occurred while solving {instance.name} with {self.name}: Method {error}")            
