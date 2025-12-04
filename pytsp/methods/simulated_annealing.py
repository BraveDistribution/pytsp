from time import time
from .utils import Instance, SolutionMethod, Tour, get_sequence_weight
from pytsp.methods.nearest_neighbor import NearestNeighbor
import numpy as np


class SimulatedAnnealing(SolutionMethod):
    """
    Author: Matej Gazda (gazda.matej@gmail.com)
    """

    def __init__(self, logging_level: int = 30, temperature: float = 1.0, n_of_iter: int = 1000, alpha: float = 0.95, max_runtime_in_sec: float = 3):
        """
        Initialize the Simulated Annealing solver.

        Args:
            logging_level (int): Controls verbosity of output. Levels: NOTSET(0), DEBUG(10), INFO(20), WARNING(30), ERROR(40), CRITICAL(50)
            temperature (float): Initial temperature.
            n_of_iter (int): Number of iterations per temperature level.
            alpha (float): Cooling rate (multiplier for temperature).
            max_runtime_in_sec (int): Max. runtime of the function (in seconds).
        """

        # Initialize core attributes for the solution method
        super().__init__(name="Simulated Annealing", 
                         info=f"max_runtime_in_sec={max_runtime_in_sec}", 
                         logging_level=logging_level)

        self.temperature = temperature
        self.n_of_iter = n_of_iter
        self.alpha = alpha
        self.max_runtime_in_sec = max_runtime_in_sec

    def solve(self, instance: Instance, tour: Tour = None) -> Tour:
        """
        Approximate the optimal path of the travelling salesman using simulated annealing.

        Args:
            instance (Instance): The TSP instance containing nodes and distances.
            tour (Tour): An initial tour to improve.

        Returns:
            Tour: A Tour object containing the improved sequence and metadata.
        """
        start_time = time()

        # Initialize tour if none is provided
        if tour is None:
            self.logger.info("Creating initial tour via Nearest Neighbor heuristic")
            tour = NearestNeighbor(logging_level=self.logger.level).solve(instance=instance)

        # Remove the last node (duplicate of the first) to work with a linear sequence
        current_sequence = tour.sequence[:-1]
        current_sequence_costs = get_sequence_weight(instance=instance, sequence=tour.sequence)

        # Track best found solution
        best_sequence = current_sequence.copy()
        best_sequence_cost = current_sequence_costs

        # Flag to track the functions runtime and stat
        sequence_has_changed = True
        initial_cost = current_sequence_costs
        count_improvements = 0

        BOLTZMANN = 5.670367e-08  # Arbitrary constant for temperature scaling

        while sequence_has_changed:
            temp_solution = current_sequence.copy()

            # Check if the time limit has been exceeded before continuing with the swap                    
            if (time() - start_time) > self.max_runtime_in_sec:
                self.logger.info(f"Stopping optimization early (time limit of {self.max_runtime_in_sec} seconds).")
                break   # Stop method

            for _ in range(self.n_of_iter):
                # Create a copy of the current sequence to modify
                next_sequence = current_sequence.copy()

                # Choose a random length for the subsequence to reverse (at least 2 elements)
                left_index = np.random.randint(2, len(current_sequence))

                # Choose a random starting index such that the subsequence fits within the array
                right_index = np.random.randint(0, len(current_sequence) - left_index)

                # Reverse the selected slice
                next_sequence[right_index:right_index + left_index] = next_sequence[
                    right_index:right_index + left_index][::-1]

                # Evaluate the new sequence
                next_sequence_costs = get_sequence_weight(
                    instance=instance,
                    sequence=next_sequence,
                    add_return_to_start=True
                )

                # Accept the new sequence
                if next_sequence_costs < current_sequence_costs:
                    # ... if it's better
                    current_sequence = next_sequence
                    current_sequence_costs = next_sequence_costs
                    
                    # Update best if improved
                    if next_sequence_costs < best_sequence_cost:
                        count_improvements += 1
                        best_sequence = next_sequence.copy()
                        best_sequence_cost = next_sequence_costs
                        
                else:
                    # ... or probabilistically worse
                    acceptance_prob = np.exp(
                        (current_sequence_costs - next_sequence_costs) / (self.temperature * BOLTZMANN)
                    )
                    if acceptance_prob > np.random.random():
                        current_sequence = next_sequence
                        current_sequence_costs = next_sequence_costs
                    
                    # Update best if improved
                    if next_sequence_costs < best_sequence_cost:
                        count_improvements += 1
                        best_sequence = next_sequence.copy()
                        best_sequence_cost = next_sequence_costs

            # Cool down the temperature
            self.temperature *= self.alpha

            # Stop if no change occurred
            if np.array_equal(temp_solution, current_sequence):
                sequence_has_changed = False
                self.logger.info(f"Stopped simulation annealing as sequences has not changed.")

        # Print statistics
        self.logger.info(f"Info (Simulated Annealing): Initial tour improved from {initial_cost} to {best_sequence_cost} after {count_improvements} improvements.")

        # Close the tour by returning to the start node
        current_sequence.append(best_sequence[0])

        # Return the final tour
        return Tour(
            instance=instance,
            solution_method=self,
            sequence=current_sequence,
            runtime_in_sec=time() - start_time
        )