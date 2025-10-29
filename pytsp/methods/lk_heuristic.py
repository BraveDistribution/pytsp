import math
from .utils import SolutionMethod, Instance, Tour, time
from lk_heuristic.models.tsp import Tsp


class LKHeuristic(SolutionMethod):
    """
    Author: Arne Heinold (arne.heinold@klu.org)

    This method integrates with the lk_heuristic project by Frederico de Castro Neto.
    GitHub: https://github.com/kikocastroneto/lk_heuristic

    License:
        This code is licensed under the MIT License.
        See the LICENSE file or visit https://opensource.org/licenses/MIT for details.  
    """

    def __init__(self, logging_level: int = 30, lk_method: str = "lk1_improve"):
        """
        Initialize the Lin Kernighan heuristic.

        Args:
            logging_level (int): Controls verbosity of output. Levels: NOTSET(0), DEBUG(10), INFO(20), WARNING(30), ERROR(40), CRITICAL(50)
            lk_method (str): The LK method to use ("lk1_improve" or "lk2_improve")
        """

        # Initialize the base class with method name and description
        super().__init__(name="Lin Kernighan", 
                         info=f"LK Method: {lk_method}", 
                         logging_level=logging_level)

        self.lk_method = lk_method

    def solve(
        self,
        instance: Instance,
        runs: int = 3,
        backtracking: tuple = (5, 5),
        reduction_level: int = 4,
        reduction_cycle: int = 4,
        tour_type: str = "cycle"
    ) -> Tour:
        """
        Solves a TSP instance using the Lin-Kernighan heuristic.

        Parameters:
            instance (Instance): The TSP problem instance.
            runs (int): Number of improvement runs.
            backtracking (tuple): Number of closest neighbors per search level.
            reduction_level (int): Level at which reduction starts.
            reduction_cycle (int): Cycle at which reduction starts.
            tour_type (str): Type of tour ('path' or 'cycle').
            logging_level (int): Logging verbosity level.

        Returns:
            Tour: The best tour found, including metadata.
        """

        # Start timing the entire solve process
        start_time = time()

        # Initialize tracking variables
        best_tour = None
        best_cost = math.inf
        mean_cost = 0

        # Map original node IDs to new zero-based IDs required by lk_heuristic
        # This ensures compatibility with libraries like TSPLIB (e.g., burma14 starts at 1)
        self.node_id_reassignment = {id: node.id for id, node in enumerate(instance.nodes)}
        self.instance = instance

        # Create the TSP object for the heuristic
        self.logger.info("Creating TSP instance")
        lk_tsp = Tsp(
            nodes=instance.nodes,
            cost_function=self.get_weight,  # Use remapped cost function
            shuffle=False,
            backtracking=backtracking,
            reduction_level=reduction_level,
            reduction_cycle=reduction_cycle,
            tour_type=tour_type,
            logging_level=self.logger.level
        )

        self.logger.info("Starting improve loop")

        # Run the heuristic multiple times to find the best tour
        for run in range(1, runs + 1):
            # Shuffle the tour nodes
            if lk_tsp.shuffle:
                lk_tsp.tour.shuffle()

            # Set initial tour cost
            lk_tsp.tour.set_cost(lk_tsp.cost_matrix)

            # Execute the selected LK improvement method
            run_start = time()
            lk_tsp.methods[self.lk_method]()
            run_end = time()

            # Update best tour if current run is better
            if lk_tsp.tour.cost < best_cost:
                best_tour = lk_tsp.tour.get_nodes()
                best_cost = lk_tsp.tour.cost

            # Update running mean cost
            mean_cost += (lk_tsp.tour.cost - mean_cost) / run

            # Log run statistics
            self.logger.info(
                f"[Run:{run}] --> Cost: {lk_tsp.tour.cost:.3f} / "
                f"Best: {best_cost:.3f} / Mean: {mean_cost:.3f} "
                f"({run_end - run_start:.3f}s)"
            )

        # Restore original node IDs
        for node in best_tour:
            node.id = self.node_id_reassignment[node.id]

        # Construct the final tour sequence (return to origin)
        sequence = best_tour + [best_tour[0]]

        # Return the final Tour object
        return Tour(
            instance=instance,
            solution_method=self,
            sequence=sequence,
            runtime_in_sec=time() - start_time
        )

    def get_weight(self, source, target):
        """
        Remaps node IDs and retrieves the weight between two nodes.

        Parameters:
            source: Source node
            target: Target node

        Returns:
            float: Weight between source and target nodes
        """
        source_id = self.node_id_reassignment[source.id]
        target_id = self.node_id_reassignment[target.id]
        return self.instance.get_weight_via_id(source_id=source_id, target_id=target_id)
