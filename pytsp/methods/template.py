from time import time
from .utils import Instance, SolutionMethod, Tour

class YourSolutionApproach(SolutionMethod):
    """
    Author: Your Name (your.mail@xyz.com)
    """

    def __init__(self, logging_level: int = 30):
        """
        Initialize the your solver.

        Args:
            logging_level (int): Controls verbosity of output. Levels: NOTSET(0), DEBUG(10), INFO(20), WARNING(30), ERROR(40), CRITICAL(50)
        """

        # Initialize core attributes for the solution method:
        # - 'name' identifies the algorithm (e.g., "Nearest Neighbor")
        # - 'info' can hold optional metadata such as time limits, parameter settings, or other configuration details
        super().__init__(name="My Method", 
                         info="All you need to know about My Method.", 
                         logging_level=logging_level)


    def solve(self, instance: Instance) -> Tour:
        """
        Solve a TSP instance using ....

        Args:
            instance (Instance): An instance of the TSP instance class.

        Returns:
            Tour: A Tour object containing the computed sequence and metadata.
        """

        # Start timing the algorithm
        start_time = time()

        # Add your code
        sequence = instance.nodes
        

        # Create and return the final tour object
        tour = Tour(
            instance=instance,
            solution_method=self,
            sequence=sequence,            
            runtime_in_sec=time() - start_time
        )

        return tour
