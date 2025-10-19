from time import time
from TSP.Tour import Tour
from TSP.Instance import Instance
from TSP.SolutionMethod import SolutionMethod
from pyvrp import Model, stop


class pyVRP(SolutionMethod):

    def __init__(self, max_runtime_in_sec: float = 60, display: bool = False):

        self.name = "pyVRP"
        self.max_runtime_in_sec = max_runtime_in_sec
        self.display = display


    def solve(self, instance: Instance) -> Tour:
        """
        Solve a TSP instance using pyVRP's Hybrid Genetic Search (HGS).

        Returns:
            Tour: A Tour object containing the computed sequence and metadata.
        """

        # Start timing the algorithm
        start_time = time()

        # Check if node coordinates are not provided in the instance
        if instance.node_coords is None:
            # Initialize default coordinates [0, 0] for each node in the instance
            node_coords = {n: [0, 0] for n in instance.nodes}
        else:
            # Use the provided node coordinates from the instance
            node_coords = instance.node_coords

        # Initialize pyVRP model
        m = Model()

        # Add vehicle (just one vehicle with sufficient capacity)
        m.add_vehicle_type(num_available=1, capacity=instance.number_of_stops)

        # Add depot
        locations = {}
        depot = instance.nodes[0]
        x_depot, y_depot = node_coords[depot] 
        locations[depot] = m.add_depot(x=x_depot, y=y_depot)

        # Add clients
        locations.update({
            n: m.add_client(x=x, y=y, delivery=1)
            for n, (x, y) in node_coords.items()
            if n != depot
        })

        # Add edges (distances between all pairs of nodes)
        for source in instance.nodes:
            for target in instance.nodes:
                distance = 0 if source == target else instance.get_weight(source, target)
                m.add_edge(locations[source], locations[target], distance=distance)

        # Solve using pyVRP
        res = m.solve(stop=stop.MaxRuntime(self.max_runtime_in_sec), display=self.display)
        solution = res.best

        # Check and extract route
        routes = solution.routes()
        if not routes:
            raise RuntimeError("Error: No routes returned by pyVRP.")

        # Build tour sequence (start and end at depot)
        sequence = [depot] + [instance.nodes[v] for v in routes[0].visits()] + [depot]

        # Create and return the final tour object
        tour = Tour(
            instance=instance,
            solution_method=self,
            sequence=sequence,            
            runtime_in_sec=time() - start_time
        )

        return tour
