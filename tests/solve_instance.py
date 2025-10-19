
from TSP.Instance import create_instance_from_file
from example_TSPLIB_experiments import get_TSPLIB_Concorde_benchmark

from Methods.nearest_neighbor import NearestNeighbor
from Methods.christofides import Christofidesx
from Methods.pyVRP import pyVRP


# Set solver
mySolver = NearestNeighbor()
# mySolver = Christofidesx()
# mySolver = pyVRP(max_runtime_in_sec=3, display=False)

# Single instance
name = 'burma14'
myTSP = create_instance_from_file(name=name, benchmark=get_TSPLIB_Concorde_benchmark(name))
myTour = mySolver.solve(instance=myTSP)
myTour.print_info()
print("")

# Multiple instances
names = ["bayg29", "brazil58"]
myTSPs = [create_instance_from_file(name=name, benchmark=get_TSPLIB_Concorde_benchmark(name))
          for name in names]
myTours = mySolver.solve_multiple_instances(list_of_instances=myTSPs)
for myTour in myTours:
    myTour.print_info()
    print("")
