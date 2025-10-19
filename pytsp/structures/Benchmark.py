
class Benchmark:
    """
    Represents a benchmark solution for a TSP instance.

    Attributes:
        name (str): Name of the benchmark.
        info (str): Information about the benchmark (e.g., source, CPU, date, etc.).
        total_weight (float): Total weight (cost) of the benchmark tour.
        runtime_in_sec (float): Time taken to compute the benchmark tour.
        sequence (list, optional): Node sequence of the benchmark tour.
    """

    def __init__(self, name: str, info: str, total_weight: float, runtime_in_sec: float, sequence: list = None):
        # Initialize benchmark attributes
        self.name = name
        self.info = info
        self.total_weight = total_weight
        self.runtime_in_sec = runtime_in_sec
        self.sequence = sequence

    def get_gap_weight(self, weight):
        """
        Compute the absolute difference in weight compared to the benchmark.

        Args:
            weight (float): Weight of the current solution.

        Returns:
            float: Absolute gap in weight.
        """
        return round(self.total_weight - weight, 4)

    def get_gap_weight_in_pct(self, weight):
        """
        Compute the percentage gap in weight compared to the benchmark.

        Args:
            weight (float): Weight of the current solution.

        Returns:
            float: Percentage gap in weight.
        """
        return round((self.total_weight - weight) / self.total_weight * 100, 4)

    def get_gap_time(self, runtime_in_sec):
        """
        Compute the absolute difference in runtime compared to the benchmark.

        Args:
            runtime_in_sec (float): Runtime of the current solution.

        Returns:
            float: Absolute gap in time.
        """
        return round(self.runtime_in_sec - runtime_in_sec, 4)

    def get_gap_time_in_pct(self, runtime_in_sec):
        """
        Compute the percentage gap in runtime compared to the benchmark.

        Args:
            runtime_in_sec (float): Runtime of the current solution.

        Returns:
            float: Percentage gap in time.
        """
        return round((self.runtime_in_sec - runtime_in_sec) / self.runtime_in_sec * 100, 4)