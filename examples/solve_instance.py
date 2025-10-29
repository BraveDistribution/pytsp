
def solve_instance():
    """
    This function provides an example of solving the Traveling Salesman Problem (TSP) using the Nearest Neighbor heuristic,
    a basic construction method that typically yields non-optimal solutions. The same usage pattern applies to other solution 
    methods available in this package.

    The demonstration includes:
    1. Solving a single TSP instance without benchmark data.
    2. Solving the same instance with benchmark data.
    3. Solving multiple TSP instances in sequence.

    Standardized tour information is printed for each scenario.
    """

    # Import necessary modules from the pytsp package
    from pytsp.structures.Instance import create_instance_from_file     # See `tests/create_instance.py` for guidance on creating TSP instances.
    from pytsp.structures.Benchmark import Benchmark                    # Class for defining benchmark values in a standardized format.
    from pytsp.methods.nearest_neighbor import NearestNeighbor          # Import the Nearest Neighbor heuristic solver.

    # Define the solver
    my_solver = NearestNeighbor()

    # --- Example 1: Solve a single instance without benchmark ---
    print("Example 1: Solve a single instance without benchmark")

    # Create a TSP instance from file
    my_instance = create_instance_from_file(name="burma14")

    # Solve the instance using the selected solver
    tour = my_solver.solve(instance=my_instance)                   

    # Print tour information
    tour.print_info()
    print("")  # Add spacing between outputs

    # Plot tour 
    fig = tour.plot()   # returns a Plotly Figure object
    fig.show()

    # --- Example 2: Solve the same instance with benchmark data ---
    print("Example 2: Solve the same instance with benchmark data")

    # Create minimal benchmark object
    benchmark = Benchmark(name="Concorde", 
                          info="See: https://www.math.uwaterloo.ca/tsp/concorde/", 
                          total_weight=3323)
    
    # Create a TSP instance from file
    my_instance = create_instance_from_file(name="burma14", benchmark=benchmark)
    
    # Solve the instance using the selected solver
    tour = my_solver.solve(instance=my_instance)

    # Print tour information
    tour.print_info()
    print("")  # Add spacing between outputs


    # --- Example 3: Solve multiple instances (without benchmark data) ---
    print("Example 3: Solve multiple instances")

    # Define set of instances
    instance_names = ["burma14", "bayg29", "brazil58"]

    # Create a list of TSP instances
    my_instances = [create_instance_from_file(name=name) for name in instance_names]

    # Solve all instances
    tours = my_solver.solve_multiple_instances(list_of_instances=my_instances)

    # Print tour information for each solved instance
    for tour in tours:
        print(f" {tour}") 
