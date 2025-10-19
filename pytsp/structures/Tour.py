from TSP import Instance
from TSP import SolutionMethod


class Tour:
    """
    Represents a solution (tour) for a TSP instance.

    Attributes:
        instance (Instance): The TSP problem instance.
        sequence (list): The ordered list of node indices representing the tour.
        solution_method (str): The name of the method used to generate the tour.
        runtime_in_sec (float or None): Time taken to compute the tour.
    """

    def __init__(self, instance: Instance, solution_method: SolutionMethod, sequence: list, runtime_in_sec: float = None):
        # Store basic tour information
        self.instance = instance
        self.solution_method = solution_method
        self.sequence = sequence        
        self.runtime_in_sec = runtime_in_sec

        # Warn if the tour length doesn't match the instance size
        if len(sequence) != instance.number_of_stops + 1:
            print(f"Warning: Tour length ({len(sequence)}) does not match instance size ({instance.number_of_stops}). Tour size should be {instance.number_of_stops + 1}")

    def get_total_weight(self):
        """
        Calculate the total weight (cost) of the tour.

        Returns:
            float: The total weight of the tour including return to the start.
        """
        # Sum weights between consecutive nodes
        total_weights = sum(
            self.instance.get_weight(self.sequence[i], self.sequence[i + 1])
            for i in range(len(self.sequence) - 1)
        )
        
        # Return weights
        return total_weights

    def plot(self):
        """
        Plot the tour using the instance's plotting method.
        """
        self.instance.plot(tour=self)
    
    def info_for_df(self):
        total_weight = self.get_total_weight()
        
        return {"instance": self.instance.name,
                "solution_method":self.solution_method.name, 
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
        print(f"  Solution method: {self.solution_method.name}")

        # Print full tour if short, otherwise abbreviated
        if len(self.sequence) <= 8:
            print(f"  Tour: {self.sequence}")
        else:
            print(
                f"  Tour: [{self.sequence[0]}, {self.sequence[1]}, {self.sequence[2]}, {self.sequence[3]}, "
                f"..., {self.sequence[-4]}, {self.sequence[-3]}, {self.sequence[-2]}, {self.sequence[-1]}]"
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
