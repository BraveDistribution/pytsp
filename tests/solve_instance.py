
def solve_instance():
    """
    This function demonstrates how to solve the Traveling Salesman Problem (TSP) using one of the package's solver.
    
    This function demonstrates solving:
    1. A single TSP instance without benchmark data.
    2. The same instance with Concorde benchmark data.
    3. Multiple TSP instances.
    
    It prints tour information for each case.
    """

    # Import necessary modules from the pytsp package
    from pytsp.structures.Instance import create_instance_from_file
    from pytsp.structures.Benchmark import Benchmark
    from pytsp.methods.nearest_neighbor import NearestNeighbor
    from pytsp.methods.christofides import Christofidesx
    from pytsp.methods.pyVRP import pyVRP

    # Choose the solver to use
    # Uncomment the desired solver
    my_solver = NearestNeighbor()
    # my_solver = Christofidesx()
    # my_solver = pyVRP(max_runtime_in_sec=3, display=True)

    # --- 1. Solve a single instance without benchmark ---
    print("1. Solve a single instance without benchmark")
    name = "burma14"
    tsp_instance = create_instance_from_file(name=name)
    tour = my_solver.solve(instance=tsp_instance)

    # Print tour information
    tour.print_info()
    print("")  # Add spacing between outputs

    # Plot tour 
    tour.plot()
    

    # --- 2. Solve the same instance with benchmark data ---
    print("2- Solve the same instance with benchmark data")
    benchmark = Benchmark(name="Concorde", info="See: https://www.math.uwaterloo.ca/tsp/concorde/", total_weight=3323)
    tsp_instance = create_instance_from_file(name=name, benchmark=benchmark)
    tour = my_solver.solve(instance=tsp_instance)

    # Print tour information with benchmark
    tour.print_info()
    print("")


    # --- 3. Solve multiple instances (without benchmark data) ---
    print("3. Solve multiple instances")
    instance_names = ["bayg29", "brazil58"]

    # Create a list of TSP instances with benchmarks
    tsp_instances = [
        create_instance_from_file(name=name)
        for name in instance_names
    ]

    # Solve all instances
    tours = my_solver.solve_multiple_instances(list_of_instances=tsp_instances)

    # Print tour information for each solved instance
    for tour in tours:
        tour.print_info()

        print("")