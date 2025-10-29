
from datetime import datetime

def get_sequence_weight(instance: "Instance", sequence: list, add_return_to_start: bool = False):
    """
    Calculate the total weight (cost) of a sequence.

    Returns:
        float: The total weight of the tour including return to the start.
    """

    local_sequence = sequence.copy()

    if add_return_to_start:
        local_sequence.append(local_sequence[0])

    # Sum weights between consecutive nodes
    total_weights = sum(
        instance.get_weight(local_sequence[i], local_sequence[i + 1])
        for i in range(len(local_sequence) - 1)
    )
    
    # Return weights
    return total_weights


class Tour:
    """
    Represents a solution (tour) for a TSP instance.

    Attributes:
        instance (Instance): The TSP problem instance.
        solution_method (str): The name of the method used to generate the tour.
        sequence (list): The ordered list of node indices representing the tour.        
        runtime_in_sec (float or None): Time taken to compute the tour.
    """

    def __init__(self, instance: "Instance", solution_method: "SolutionMethod", sequence: list, runtime_in_sec: float = None):
        # Store basic tour information
        self.instance = instance
        self.solution_method = solution_method
        self.sequence = sequence        
        self.runtime_in_sec = runtime_in_sec

        # Warn if the tour length doesn't match the instance size
        if len(sequence) != instance.number_of_stops + 1:
            solution_method.logger.warning(f"Tour length ({len(sequence)}) does not match instance size ({instance.number_of_stops}). Tour size should be {instance.number_of_stops + 1}")

    def get_total_weight(self):
        """
        Calculate the total weight (cost) of the tour.

        Returns:
            float: The total weight of the tour including return to the start.
        """

        return get_sequence_weight(instance=self.instance, sequence=self.sequence)

    def plot(self):
        """
        Plot the tour using the instance's plotting method.
        """
        return self.instance.plot(tour=self)
    
    def info_for_df(self):
        """
            Collects key information about the tour and returns it as a dictionary
            for easy conversion into a pandas DataFrame.

            Returns:
                dict: A dictionary containing:
                    - instance (str): Name of the TSP instance.
                    - solution_method (str): Name of the solver used.
                    - solution_method_info (str): Info of the solver used.
                    - date_time ()
                    - total_weights (float): Total weight of the computed tour (rounded to 4 decimals).
                    - run_time_in_sec (float): Runtime in seconds (rounded to 4 decimals).
                    - benchmark_name (str or None): Name of the benchmark if available.
                    - gap_to_benchmark (float or None): Absolute gap to benchmark weight.
                    - gap_to_benchmark_in_pct (float or None): Gap to benchmark in percentage.
            """

        # Get the total weight of the computed tour
        total_weight = self.get_total_weight()
        
        # Build and return a dictionary with all relevant information
        return {"instance": self.instance.name,
                "solution_method":self.solution_method.name, 
                "solution_method_info":self.solution_method.info, 
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_weights": round(total_weight, 4),
                "run_time_in_sec": round(self.runtime_in_sec, 4),
                "benchmark_name": None if self.instance.benchmark is None else self.instance.benchmark.name, 
                "gap_to_benchmark": None if self.instance.benchmark is None else self.instance.benchmark.get_gap_weight(total_weight),
                "gap_to_benchmark_in_pct": None if self.instance.benchmark is None else self.instance.benchmark.get_gap_weight_in_pct(total_weight)
                }

    def print_info(self):
        """
        Print detailed information about the tour.
        """
        print(f"Instance: {self.instance.name}")
        print(f"  Solution method: {self.solution_method.name} ({self.solution_method.info})")

        # Print full tour if short, otherwise abbreviated
        if len(self.sequence) <= 8:
            print(f"  Tour: {[n.id for n in self.sequence]}")
        else:
            print(
                f"  Tour: [{self.sequence[0].id}, {self.sequence[1].id}, {self.sequence[2].id}, {self.sequence[3].id}, "
                f"..., {self.sequence[-4].id}, {self.sequence[-3].id}, {self.sequence[-2].id}, {self.sequence[-1].id}]"
            )

        # Print total weight and benchmark gap if available
        total_weight = round(self.get_total_weight(), 2)
        if self.instance.benchmark is not None:
            gap = self.instance.benchmark.get_gap_weight_in_pct(self.get_total_weight())
            print(f"  Total weight: {total_weight} | Gap to {self.instance.benchmark.name}: {gap}%")
        else:
            print(f"  Total weight: {total_weight}")

        # Print runtime
        print(f"  Runtime: {round(self.runtime_in_sec, 4)} seconds")

    def __str__(self):
        """
        Return a string summary of the tour.

        Returns:
            str: Summary including instance name, method, weight, and runtime.
        """
        return (
            f"Instance: {self.instance.name}, "
            f"Solution method: {self.solution_method.name}, "
            f"Total weight: {round(self.get_total_weight(), 2)}, "
            f"Runtime: {round(self.runtime_in_sec, 4)} seconds"
        )
