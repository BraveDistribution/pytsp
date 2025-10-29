import unittest


class UnitTests(unittest.TestCase):

    def test_create_instance_from_file(self):
                
        from pytsp.structures.Instance import create_instance_from_file

        # Load fromt he pytsp/data/TSPLIB folder
        my_instance = create_instance_from_file(name='burma14')

        # Check weight of one of the edges
        self.assertEqual(my_instance.get_weight_via_id(source_id=1, target_id=2), 153)

    def test_create_instance_from_coordinates(self):
        from pytsp.structures.Instance import create_instance_from_coordinates

        # Coordinates for the burma14 instance
        burma14_coordinates = [
            (16.47, 96.10),
            (16.47, 94.44),
            (20.09, 92.54),
            (22.39, 93.37),
            (25.23, 97.24),
            (22.00, 96.05),
            (20.47, 97.02),
            (17.20, 96.29),
            (16.30, 97.38),
            (14.05, 98.12),
            (16.53, 97.38),
            (21.52, 95.59),
            (19.41, 97.13),
            (20.09, 94.55)
        ]

        # Create instance from coordinates (weights as specified in the burma14 TSPLIB file)
        my_instance = create_instance_from_coordinates(name='burma14_coordinates', 
                                                coordinates=burma14_coordinates,
                                                edge_weight_type="GEO",        
                                                edge_weight_format="FUNCTION"  
                                                )
        
        # Check weight of one of the edges
        self.assertEqual(my_instance.get_weight_via_id(source_id=1, target_id=2), 153)
        
    def test_create_instance_from_matrix(self):
        from pytsp.structures.Instance import create_instance_from_cost_matrix

        # Precomputed cost matrix for burma14
        burma14_cost_matrix = [
            [1, 153, 510, 706, 966, 581, 455, 70, 160, 372, 157, 567, 342, 398],
            [153, 1, 422, 664, 997, 598, 507, 197, 311, 479, 310, 581, 417, 376],
            [510, 422, 1, 289, 744, 390, 437, 491, 645, 880, 618, 374, 455, 211],
            [706, 664, 289, 1, 491, 265, 410, 664, 804, 1070, 768, 259, 499, 310],
            [966, 997, 744, 491, 1, 400, 514, 902, 990, 1261, 947, 418, 635, 636],
            [581, 598, 390, 265, 400, 1, 168, 522, 634, 910, 593, 19, 284, 239],
            [455, 507, 437, 410, 514, 168, 1, 389, 482, 757, 439, 163, 124, 232],
            [70, 197, 491, 664, 902, 522, 389, 1, 154, 406, 133, 508, 273, 355],
            [160, 311, 645, 804, 990, 634, 482, 154, 1, 276, 43, 623, 358, 498],
            [372, 479, 880, 1070, 1261, 910, 757, 406, 276, 1, 318, 898, 633, 761],
            [157, 310, 618, 768, 947, 593, 439, 133, 43, 318, 1, 582, 315, 464],
            [567, 581, 374, 259, 418, 19, 163, 508, 623, 898, 582, 1, 275, 221],
            [342, 417, 455, 499, 635, 284, 124, 273, 358, 633, 315, 275, 1, 247],
            [398, 376, 211, 310, 636, 239, 232, 355, 498, 761, 464, 221, 247, 1]
        ]

        # Create instance from cost matrix (weights as computed via the GEO distance functions specified in the burma14 TSPLIB file)
        my_instance = create_instance_from_cost_matrix(name="burma14_matrix", cost_matrix=burma14_cost_matrix)

        # Check weight of one of the edges
        self.assertEqual(my_instance.get_weight_via_id(source_id=0, target_id=1), 153)
    
    def test_solve_christofides(self):
        from pytsp.structures.Instance import create_instance_from_file
        from pytsp.methods.christofides import Christofidesx

        # Load fromt he pytsp/data/TSPLIB folder
        my_instance = create_instance_from_file(name='burma14')
        
        # Solve instance
        my_solver = Christofidesx(logging_level=50)
        tour = my_solver.solve(instance=my_instance)
        self.assertEqual(tour.get_total_weight(), 3606)
    
    def test_solve_three_opt(self):
        from pytsp.structures.Instance import create_instance_from_file
        from pytsp.methods.k_opt import ThreeOpt

        # Load fromt he pytsp/data/TSPLIB folder
        my_instance = create_instance_from_file(name='burma14')

        # Solve instance
        my_solver = ThreeOpt(logging_level=50, max_runtime_in_sec=3)
        tour = my_solver.solve(instance=my_instance)
        self.assertEqual(tour.get_total_weight(), 3336)

    def test_solve_two_opt(self):
        from pytsp.structures.Instance import create_instance_from_file
        from pytsp.methods.k_opt import TwoOpt

        # Load fromt he pytsp/data/TSPLIB folder
        my_instance = create_instance_from_file(name='burma14')
        
        # Solve instance
        my_solver = TwoOpt(logging_level=50, max_runtime_in_sec=3)
        tour = my_solver.solve(instance=my_instance)
        self.assertEqual(tour.get_total_weight(), 4040)
    
    def test_solve_lk_heuristic(self):
        from pytsp.structures.Instance import create_instance_from_file
        from pytsp.methods.lk_heuristic import LKHeuristic

        # Load fromt he pytsp/data/TSPLIB folder
        my_instance = create_instance_from_file(name='burma14')
        
        # Solve instance LK1
        my_solver = LKHeuristic(logging_level=50, lk_method="lk1_improve")
        tour = my_solver.solve(instance=my_instance)
        self.assertIsInstance(tour.get_total_weight(), int) # Assert only the type, since LKHeuristic's inherent randomness may affect the value.

        # Solve instance LK2
        my_solver = LKHeuristic(logging_level=50, lk_method="lk2_improve")
        tour = my_solver.solve(instance=my_instance)
        self.assertIsInstance(tour.get_total_weight(), int) # Assert only the type, since LKHeuristic's inherent randomness may affect the value.

    def test_solve_nearest_neighbor(self):
        from pytsp.structures.Instance import create_instance_from_file
        from pytsp.methods.nearest_neighbor import NearestNeighbor

        # Load fromt he pytsp/data/TSPLIB folder
        my_instance = create_instance_from_file(name='burma14')
        
        # Solve instance
        my_solver = NearestNeighbor(logging_level=50)
        tour = my_solver.solve(instance=my_instance)
        self.assertEqual(tour.get_total_weight(), 4048)
    
    def test_solve_permutation(self):
        from pytsp.structures.Instance import create_instance_from_file
        from pytsp.methods.permutations import Permutations

        # Load fromt he pytsp/data/TSPLIB folder
        my_instance = create_instance_from_file(name='burma14')
        
        # Solve instance
        my_solver = Permutations(logging_level=50)
        tour = my_solver.solve(instance=my_instance, max_nodes=5)
        self.assertEqual(tour.get_total_weight(), 2321)
    
    def test_solve_pyVRP(self):
        from pytsp.structures.Instance import create_instance_from_file
        from pytsp.methods.pyVRP import pyVRP

        # Load fromt he pytsp/data/TSPLIB folder
        my_instance = create_instance_from_file(name='burma14')
        
        # Solve instance
        my_solver = pyVRP(logging_level=50, max_runtime_in_sec=1)
        tour = my_solver.solve(instance=my_instance)
        self.assertIsInstance(tour.get_total_weight(), int) # Assert only the type, since pyVRP's inherent randomness may affect the value.
    
    def test_solve_simulated_annealing(self):
        from pytsp.structures.Instance import create_instance_from_file
        from pytsp.methods.simulated_annealing import SimulatedAnnealing

        # Load fromt he pytsp/data/TSPLIB folder
        my_instance = create_instance_from_file(name='burma14')
        
        # Solve instance
        my_solver = SimulatedAnnealing(logging_level=50, max_runtime_in_sec=1)
        tour = my_solver.solve(instance=my_instance)
        self.assertIsInstance(tour.get_total_weight(), int) # Assert only the type, since simulated annealings's inherent randomness may affect the value.
    
    def test_simple_experiment(self):        
        from pytsp.structures.Experiment import Experiment
        from pytsp.structures.Instance import create_instance_from_file

        from pytsp.methods.nearest_neighbor import NearestNeighbor
        from pytsp.methods.christofides import Christofidesx

        import pandas as pd

        # Define experiment
        my_experiment = Experiment(
            name="Unit Test: Two solvers and two instance",
            list_of_instances=[create_instance_from_file(name='burma14'), 
                               create_instance_from_file(name='bayg29')],
            list_of_solution_methods=[NearestNeighbor(), 
                                      Christofidesx()],
            logging_level=50 # Controls verbosity of output. Levels: NOTSET(0), DEBUG(10), INFO(20), WARNING(30), ERROR(40), CRITICAL(50)
        )

        # Execute the experiment
        my_experiment.run()        
        self.assertIsInstance(my_experiment.df_results, pd.DataFrame) # Assert the type, which should be a dataframe
        self.assertEqual(len(my_experiment.df_results), 4) # Assert the type, which should be a dataframe


if __name__ == '__main__':
    unittest.main(verbosity=2)