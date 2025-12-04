from time import time
from .utils import Instance, SolutionMethod, Tour, get_sequence_weight
from pytsp.methods.nearest_neighbor import NearestNeighbor
from enum import Enum
import numpy as np

class TwoOpt(SolutionMethod):
    """
    Author: Matej Gazda (gazda.matej@gmail.com)
    """

    def __init__(self, logging_level: int = 30, max_runtime_in_sec: float = 3):
        """
        Initialize the 2-Opt heuristic.

        Args:
            logging_level (int): Controls verbosity of output. Levels: NOTSET(0), DEBUG(10), INFO(20), WARNING(30), ERROR(40), CRITICAL(50)
            max_runtime_in_sec (int): Max. runtime in seconds
        """

        # Initialize core attributes for the solution method
        super().__init__(name="2-opt", 
                         info=f"max_runtime_in_sec={max_runtime_in_sec}", 
                         logging_level=logging_level)

        self.max_runtime_in_sec = max_runtime_in_sec


    def solve(self, instance: Instance, tour: Tour = None) -> Tour:
        """
        Approximate the optimal path of the travelling salesman using the 2-opt algorithm.

        Args:
            instance (Instance): The TSP instance containing nodes and distances.
            tour (Tour): An initial tour to improve.

        Returns:
            Tour: A Tour object containing the improved sequence and metadata.
        """

        # Start timing the algorithm
        start_time = time()
 
        # Initialize tour if none is provided
        if tour is None:
            self.logger.info("Creating initial tour via Nearest Neighbor heuristic")
            tour = NearestNeighbor(logging_level=self.logger.level).solve(instance=instance)

        # Initialize the best known route and its cost
        best_found_route = np.array(tour.sequence[:-1]) # Convert the initial tour (excluding the return to start) to a NumPy array
        best_found_route_cost = get_sequence_weight(instance=instance, sequence=tour.sequence)

        # Flag to track the functions runtime, improvements, and stat
        improved = True
        below_max_runtime = True
        initial_cost = best_found_route_cost
        count_improvements = 0

        # Repeat optimization until no improvement or time limit is reached
        while improved and below_max_runtime:
            improved = False
            best_candidate_route = best_found_route.copy()
            best_candidate_cost = best_found_route_cost

            # Try all possible 2-opt swaps (i, k) where i < k
            for i in range(1, len(best_found_route) - 1):
                if improved or not below_max_runtime:
                    break   # Restart outer loop after improvement or break after time limit

                for k in range(i + 1, len(best_found_route) - 1):
                    # Check if the time limit has been exceeded before continuing with the swap                    
                    if (time() - start_time) > self.max_runtime_in_sec:
                        self.logger.info(f"Stopping optimization early (time limit of {self.max_runtime_in_sec} seconds).")
                        below_max_runtime = False
                        break   # Stop method

                    # Perform 2-opt swap: reverse the segment between i and k
                    new_route = np.concatenate((
                        best_found_route[:i],               # segment before i
                        best_found_route[i:k + 1][::-1],    # reversed segment i to k
                        best_found_route[k + 1:]            # segment after k
                    ))

                    # Calculate the cost of the new route
                    new_route_cost = get_sequence_weight(
                        instance=instance,
                        sequence=new_route.tolist(),
                        add_return_to_start=True
                    )

                    # If the new route is better, keep it as the best candidate
                    if new_route_cost < best_candidate_cost:
                        best_candidate_cost = new_route_cost
                        best_candidate_route = new_route.copy()
                        improved = True
                        count_improvements += 1
                        break   # Restart outer loop after improvement

            # If any improvement was found, update the best known route
            if improved:
                best_found_route = best_candidate_route.copy()
                best_found_route_cost = best_candidate_cost
        
        # Add the starting node to the end to complete the cycle
        best_found_route = np.append(best_found_route, best_found_route[0])

        # Print statistics
        self.logger.info(f"Initial tour improved from {initial_cost} to {best_candidate_cost} after {count_improvements} improvements.")

        # Create and return the final Tour object
        return Tour(
            instance=instance,
            solution_method=self,
            sequence=best_found_route.tolist(),
            runtime_in_sec=time() - start_time
        )


class ThreeOpt(SolutionMethod):
    """
    Author: Matej Gazda (gazda.matej@gmail.com)
    """
    
    def __init__(self, logging_level: int = 30, max_runtime_in_sec: float = 3):
        """
        Initialize the 3-Opt heuristic.

        Args:
            logging_level (int): Controls verbosity of output. Levels: NOTSET(0), DEBUG(10), INFO(20), WARNING(30), ERROR(40), CRITICAL(50)
            max_runtime_in_sec (int): Max. runtime in seconds
        """

        # Initialize core attributes for the solution method
        super().__init__(name="3-opt", 
                         info=f"max_runtime_in_sec={max_runtime_in_sec}", 
                         logging_level=logging_level)

        self.max_runtime_in_sec = max_runtime_in_sec

    def solve(self, instance: Instance, tour: Tour = None) -> Tour:
        """
        Approximate the optimal path of the travelling salesman using the 3-opt algorithm.

        Args:
            instance (Instance): The TSP instance containing nodes and distances.
            tour (Tour): An initial tour to improve.

        Returns:
            Tour: A Tour object containing the improved sequence and metadata.
        """

        # Start timing the algorithm
        start_time = time()

        # Initialize tour if none is provided
        if tour is None:
            self.logger.info("Creating initial tour via Nearest Neighbor heuristic")
            tour = NearestNeighbor(logging_level=self.logger.level).solve(instance=instance)

        # Convert the initial tour to a NumPy array (excluding the return to start)
        route = np.array(tour.sequence[:-1])

        # Initialize cost tracking for each 3-opt case
        moves_cost = {opt_case: 0 for opt_case in OptCase}

        # Initialize improvement flag and best known route
        improved = True
        best_found_route = route.copy()

        # Flag to track the functions runtime and stat
        below_max_runtime = True
        initial_cost = get_sequence_weight(instance=instance, sequence=tour.sequence)
        count_improvements = 0

        # Optimization loop
        while improved and below_max_runtime:
            improved = False

            # Iterate over all valid segment combinations
            for i, j, k in possible_segments(len(route)):
                # Check if the time limit has been exceeded before continuing with the swap                    
                if (time() - start_time) > self.max_runtime_in_sec:
                    self.logger.info(f"Stopping optimization early (time limit of {self.max_runtime_in_sec} seconds).")
                    below_max_runtime = False
                    break   # Stop method

                # Evaluate all 3-opt cases for the current segment
                for opt_case in OptCase:
                    moves_cost[opt_case] = get_solution_cost_change(
                        instance,
                        best_found_route.tolist(),
                        opt_case,
                        i,
                        j,
                        k
                    )

                # Select the best move (maximum cost reduction)
                best_return = max(moves_cost, key=moves_cost.get)

                # Apply the move if it improves the route
                if moves_cost[best_return] > 0:
                    best_found_route = np.array(reverse_segments(
                        best_found_route.tolist(),
                        best_return,
                        i,
                        j,
                        k
                    ))
                    improved = True
                    count_improvements += 1
                    break  # Restart outer loop after improvement

        
        # Add the starting node to the end to complete the cycle
        best_found_route = np.append(best_found_route, best_found_route[0]).tolist()

        # Print statistics
        self.logger.info(f"Initial tour improved from {initial_cost} to {get_sequence_weight(instance=instance, 
                                                                                      sequence=best_found_route)} after {count_improvements} improvements.")

        # Create and return the final Tour object
        return Tour(
            instance=instance,
            solution_method=self,
            sequence=best_found_route,
            runtime_in_sec=time() - start_time
        )


class OptCase(Enum):
    """
    Enumeration of the 8 possible 3-opt move cases.
    Each case represents a different way to reconnect three segments.
    """
    OPT_CASE_1 = "opt_case_1"  # No change (original route)
    OPT_CASE_2 = "opt_case_2"  # Reverse segment A
    OPT_CASE_3 = "opt_case_3"  # Reverse segment C
    OPT_CASE_4 = "opt_case_4"  # Reverse segments A and C
    OPT_CASE_5 = "opt_case_5"  # Reverse segments A and B
    OPT_CASE_6 = "opt_case_6"  # Reverse segment B
    OPT_CASE_7 = "opt_case_7"  # Reverse segments B and C
    OPT_CASE_8 = "opt_case_8"  # Reverse all segments


def possible_segments(n):
    """
    Generate all valid (i, j, k) segment combinations for 3-opt.

    Args:
        n (int): Number of nodes in the route.

    Returns:
        generator: Yields tuples of (i, j, k) indices.
    """
    return (
        (i, j, k)
        for i in range(n)
        for j in range(i + 2, n - 1)
        for k in range(j + 2, n - 1 + (i > 0))
    )


def get_solution_cost_change(instance, route, case, i, j, k):
    """
    Compute the cost difference for a given 3-opt move.

    Args:
        instance (Instance): TSP instance with weight function.
        route (list): Current route as a list of node indices.
        case (OptCase): The 3-opt case to evaluate.
        i, j, k (int): Indices defining the segments.

    Returns:
        float: Cost improvement (positive means better).
    """
    # Identify segment endpoints
    A, B = route[i - 1], route[i]
    C, D = route[j - 1], route[j]
    E, F = route[k - 1], route[k % len(route)]

    # Evaluate cost change for each 3-opt case
    if case == OptCase.OPT_CASE_1:
        return 0  # No change
    elif case == OptCase.OPT_CASE_2:
        return instance.get_weight(A, B) + instance.get_weight(E, F) - (
            instance.get_weight(B, F) + instance.get_weight(A, E)
        )
    elif case == OptCase.OPT_CASE_3:
        return instance.get_weight(C, D) + instance.get_weight(E, F) - (
            instance.get_weight(D, F) + instance.get_weight(C, E)
        )
    elif case == OptCase.OPT_CASE_4:
        return instance.get_weight(A, B) + instance.get_weight(C, D) + instance.get_weight(E, F) - (
            instance.get_weight(A, D) + instance.get_weight(B, F) + instance.get_weight(E, C)
        )
    elif case == OptCase.OPT_CASE_5:
        return instance.get_weight(A, B) + instance.get_weight(C, D) + instance.get_weight(E, F) - (
            instance.get_weight(C, F) + instance.get_weight(B, D) + instance.get_weight(E, A)
        )
    elif case == OptCase.OPT_CASE_6:
        return instance.get_weight(B, A) + instance.get_weight(D, C) - (
            instance.get_weight(C, A) + instance.get_weight(B, D)
        )
    elif case == OptCase.OPT_CASE_7:
        return instance.get_weight(A, B) + instance.get_weight(C, D) + instance.get_weight(E, F) - (
            instance.get_weight(B, E) + instance.get_weight(D, F) + instance.get_weight(C, A)
        )
    elif case == OptCase.OPT_CASE_8:
        return instance.get_weight(A, B) + instance.get_weight(C, D) + instance.get_weight(E, F) - (
            instance.get_weight(A, D) + instance.get_weight(C, F) + instance.get_weight(B, E)
        )


def reverse_segments(route, case, i, j, k):
    """
    Apply a 3-opt move to the route based on the given case.

    Args:
        route (list): Current route as a list of node indices.
        case (OptCase): The 3-opt case to apply.
        i, j, k (int): Indices defining the segments.

    Returns:
        list: New route after applying the move.
    """
    n = len(route)

    # Handle wrap-around for circular route
    if (i - 1) < (k % n):
        first_segment = route[k % n:] + route[:i]
    else:
        first_segment = route[k % n:i]

    second_segment = route[i:j]
    third_segment = route[j:k]

    # Apply the appropriate reversal pattern
    if case == OptCase.OPT_CASE_1:
        return route  # No change
    elif case == OptCase.OPT_CASE_2:
        return list(reversed(first_segment)) + second_segment + third_segment
    elif case == OptCase.OPT_CASE_3:
        return first_segment + second_segment + list(reversed(third_segment))
    elif case == OptCase.OPT_CASE_4:
        return list(reversed(first_segment)) + second_segment + list(reversed(third_segment))
    elif case == OptCase.OPT_CASE_5:
        return list(reversed(first_segment)) + list(reversed(second_segment)) + third_segment
    elif case == OptCase.OPT_CASE_6:
        return first_segment + list(reversed(second_segment)) + third_segment
    elif case == OptCase.OPT_CASE_7:
        return first_segment + list(reversed(second_segment)) + list(reversed(third_segment))
    elif case == OptCase.OPT_CASE_8:
        return list(reversed(first_segment)) + list(reversed(second_segment)) + list(reversed(third_segment))
