from TSP.Instance import create_instance_from_file
from TSP.Benchmark import Benchmark

# Importing available solving methods
from Methods.nearest_neighbor import NearestNeighbor
from Methods.christofides import Christofidesx
from Methods.pyVRP import pyVRP

import pandas as pd
import plotly.express as px
from typing import Literal
from pyparsing import Path


# Source: https://www.math.uwaterloo.ca/tsp/concorde/benchmarks/bench.html
TSPLIB_CONCORDE_BENCHMARKS = {
     'a280': {'total_weight': 2579, 'runtime_in_sec': 5.37, 'dimension': 280}, 'ali535': {'total_weight': 202339, 'runtime_in_sec': 53.14, 'dimension': 535}, 'att48': {'total_weight': 10628, 'runtime_in_sec': 0.56, 'dimension': 48}, 'att532': {'total_weight': 27686, 'runtime_in_sec': 109.52, 'dimension': 532}, 'bayg29': {'total_weight': 1610, 'runtime_in_sec': 0.09, 'dimension': 29}, 'bays29': {'total_weight': 2020, 'runtime_in_sec': 0.13, 'dimension': 29}, 'berlin52': {'total_weight': 7542, 'runtime_in_sec': 0.29, 'dimension': 52}, 'bier127': {'total_weight': 118282, 'runtime_in_sec': 1.65, 'dimension': 127}, 'brazil58': {'total_weight': 25395, 'runtime_in_sec': 0.68, 'dimension': 58}, 'brd14051': {'total_weight': 469385, 'runtime_in_sec': 'OPEN', 'dimension': 14051}, 'brg180': {'total_weight': 1950, 'runtime_in_sec': 1.46, 'dimension': 180}, 'burma14': {'total_weight': 3323, 'runtime_in_sec': 0.06, 'dimension': 14}, 'ch130': {'total_weight': 6110, 'runtime_in_sec': 2.13, 'dimension': 130}, 'ch150': {'total_weight': 6528, 'runtime_in_sec': 3.03, 'dimension': 150}, 'd198': {'total_weight': 15780, 'runtime_in_sec': 11.82, 'dimension': 198}, 'd493': {'total_weight': 35002, 'runtime_in_sec': 113.32, 'dimension': 493}, 'd657': {'total_weight': 48912, 'runtime_in_sec': 260.37, 'dimension': 657}, 'd1291': {'total_weight': 50801, 'runtime_in_sec': 27393.72, 'dimension': 1291}, 'd1655': {'total_weight': 62128, 'runtime_in_sec': 263.03, 'dimension': 1655}, 'd2103': {'total_weight': 80450, 'runtime_in_sec': 11179253.91, 'dimension': 2103}, 'd15112': {'total_weight': 1573084, 'runtime_in_sec': '~22.6 years', 'dimension': 15112}, 'd18512': {'total_weight': 645238, 'runtime_in_sec': 'OPEN', 'dimension': 18512}, 'dantzig42': {'total_weight': 699, 'runtime_in_sec': 0.23, 'dimension': 42}, 'dsj1000': {'total_weight': 18659688, 'runtime_in_sec': 410.32, 'dimension': 1000}, 'eil51': {'total_weight': 426, 'runtime_in_sec': 0.73, 'dimension': 51}, 'eil76': {'total_weight': 538, 'runtime_in_sec': 0.3, 'dimension': 76}, 'eil101': {'total_weight': 629, 'runtime_in_sec': 0.74, 'dimension': 101}, 'fl417': {'total_weight': 11861, 'runtime_in_sec': 57.75, 'dimension': 417}, 'fl1400': {'total_weight': 20127, 'runtime_in_sec': 1548.51, 'dimension': 1400}, 'fl1577': {'total_weight': 22249, 'runtime_in_sec': 6705.04, 'dimension': 1577}, 'fl3795': {'total_weight': 28772, 'runtime_in_sec': 69886.48, 'dimension': 3795}, 'fnl4461': {'total_weight': 182566, 'runtime_in_sec': 53420.13, 'dimension': 4461}, 'fri26': {'total_weight': 937, 'runtime_in_sec': 0.07, 'dimension': 26}, 'gil262': {'total_weight': 2378, 'runtime_in_sec': 13.06, 'dimension': 262}, 'gr17': {'total_weight': 2085, 'runtime_in_sec': 0.08, 'dimension': 17}, 'gr21': {'total_weight': 2707, 'runtime_in_sec': 0.03, 'dimension': 21}, 'gr24': {'total_weight': 1272, 'runtime_in_sec': 0.07, 'dimension': 24}, 'gr48': {'total_weight': 5046, 'runtime_in_sec': 0.67, 'dimension': 48}, 'gr96': {'total_weight': 55209, 'runtime_in_sec': 6.71, 'dimension': 96}, 'gr120': {'total_weight': 6942, 'runtime_in_sec': 2.23, 'dimension': 120}, 'gr137': {'total_weight': 69853, 'runtime_in_sec': 3.42, 'dimension': 137}, 'gr202': {'total_weight': 40160, 'runtime_in_sec': 5.01, 'dimension': 202}, 'gr229': {'total_weight': 134602, 'runtime_in_sec': 38.61, 'dimension': 229}, 'gr431': {'total_weight': 171414, 'runtime_in_sec': 133.29, 'dimension': 431}, 'gr666': {'total_weight': 294358, 'runtime_in_sec': 49.86, 'dimension': 666}, 'hk48': {'total_weight': 11461, 'runtime_in_sec': 0.17, 'dimension': 48}, 'kroA100': {'total_weight': 21282, 'runtime_in_sec': 1.0, 'dimension': 100}, 'kroB100': {'total_weight': 22141, 'runtime_in_sec': 2.36, 'dimension': 100}, 'kroC100': {'total_weight': 20749, 'runtime_in_sec': 0.96, 'dimension': 100}, 'kroD100': {'total_weight': 21294, 'runtime_in_sec': 1.0, 'dimension': 100}, 'kroE100': {'total_weight': 22068, 'runtime_in_sec': 2.44, 'dimension': 100}, 'kroA150': {'total_weight': 26524, 'runtime_in_sec': 5.0, 'dimension': 150}, 'kroB150': {'total_weight': 26130, 'runtime_in_sec': 4.23, 'dimension': 150}, 'kroA200': {'total_weight': 29368, 'runtime_in_sec': 6.59, 'dimension': 200}, 'kroB200': {'total_weight': 29437, 'runtime_in_sec': 3.91, 'dimension': 200}, 'lin105': {'total_weight': 14379, 'runtime_in_sec': 0.59, 'dimension': 105}, 'lin318': {'total_weight': 42029, 'runtime_in_sec': 9.74, 'dimension': 318}, 'linhp318': {'total_weight': 41345, 'runtime_in_sec': '', 'dimension': 318}, 'nrw1379': {'total_weight': 56638, 'runtime_in_sec': 578.42, 'dimension': 1379}, 'p654': {'total_weight': 34643, 'runtime_in_sec': 26.52, 'dimension': 654}, 'pa561': {'total_weight': 2763, 'runtime_in_sec': 246.82, 'dimension': 561}, 'pcb442': {'total_weight': 50778, 'runtime_in_sec': 49.92, 'dimension': 442}, 'pcb1173': {'total_weight': 56892, 'runtime_in_sec': 468.27, 'dimension': 1173}, 'pcb3038': {'total_weight': 137694, 'runtime_in_sec': 80828.87, 'dimension': 3038}, 'pla7397': {'total_weight': 23260728, 'runtime_in_sec': 428996.2, 'dimension': 7397}, 'pla33810': {'total_weight': 66048945, 'runtime_in_sec': 'OPEN', 'dimension': 33810}, 'pla85900': {'total_weight': 142382641, 'runtime_in_sec': 'OPEN', 'dimension': 85900}, 'pr76': {'total_weight': 108159, 'runtime_in_sec': 1.86, 'dimension': 76}, 'pr107': {'total_weight': 44303, 'runtime_in_sec': 1.03, 'dimension': 107}, 'pr124': {'total_weight': 59030, 'runtime_in_sec': 3.64, 'dimension': 124}, 'pr136': {'total_weight': 96772, 'runtime_in_sec': 3.97, 'dimension': 136}, 'pr144': {'total_weight': 58537, 'runtime_in_sec': 2.58, 'dimension': 144}, 'pr152': {'total_weight': 73682, 'runtime_in_sec': 7.93, 'dimension': 152}, 'pr226': {'total_weight': 80369, 'runtime_in_sec': 4.35, 'dimension': 226}, 'pr264': {'total_weight': 49135, 'runtime_in_sec': 2.67, 'dimension': 264}, 'pr299': {'total_weight': 48191, 'runtime_in_sec': 17.49, 'dimension': 299}, 'pr439': {'total_weight': 107217, 'runtime_in_sec': 216.75, 'dimension': 439}, 'pr1002': {'total_weight': 259045, 'runtime_in_sec': 34.3, 'dimension': 1002}, 'pr2392': {'total_weight': 378032, 'runtime_in_sec': 116.86, 'dimension': 2392}, 'rat99': {'total_weight': 1211, 'runtime_in_sec': 0.95, 'dimension': 99}, 'rat195': {'total_weight': 2323, 'runtime_in_sec': 22.23, 'dimension': 195}, 'rat575': {'total_weight': 6773, 'runtime_in_sec': 363.07, 'dimension': 575}, 'rat783': {'total_weight': 8806, 'runtime_in_sec': 37.88, 'dimension': 783}, 'rd100': {'total_weight': 7910, 'runtime_in_sec': 0.67, 'dimension': 100}, 'rd400': {'total_weight': 15281, 'runtime_in_sec': 148.42, 'dimension': 400}, 'rl1304': {'total_weight': 252948, 'runtime_in_sec': 189.2, 'dimension': 1304}, 'rl1323': {'total_weight': 270199, 'runtime_in_sec': 3742.25, 'dimension': 1323}, 'rl1889': {'total_weight': 316536, 'runtime_in_sec': 10023.02, 'dimension': 1889}, 'rl5915': {'total_weight': 565530, 'runtime_in_sec': 2319671.71, 'dimension': 5915}, 'rl5934': {'total_weight': 556045, 'runtime_in_sec': 588936.85, 'dimension': 5934}, 'rl11849': {'total_weight': 923288, 'runtime_in_sec': '~155 days', 'dimension': 11849}, 'si175': {'total_weight': 21407, 'runtime_in_sec': 13.09, 'dimension': 175}, 'si535': {'total_weight': 48450, 'runtime_in_sec': 43.13, 'dimension': 535}, 'si1032': {'total_weight': 92650, 'runtime_in_sec': 25.47, 'dimension': 1032}, 'st70': {'total_weight': 675, 'runtime_in_sec': 0.5, 'dimension': 70}, 'swiss42': {'total_weight': 1273, 'runtime_in_sec': 0.13, 'dimension': 42}, 'ts225': {'total_weight': 126643, 'runtime_in_sec': 20.52, 'dimension': 225}, 'tsp225': {'total_weight': 3916, 'runtime_in_sec': 15.01, 'dimension': 225}, 'u159': {'total_weight': 42080, 'runtime_in_sec': 1.0, 'dimension': 159}, 'u574': {'total_weight': 36905, 'runtime_in_sec': 23.04, 'dimension': 574}, 'u724': {'total_weight': 41910, 'runtime_in_sec': 225.44, 'dimension': 724}, 'u1060': {'total_weight': 224094, 'runtime_in_sec': 571.43, 'dimension': 1060}, 'u1432': {'total_weight': 152970, 'runtime_in_sec': 223.7, 'dimension': 1432}, 'u1817': {'total_weight': 57201, 'runtime_in_sec': 449230.55, 'dimension': 1817}, 'u2152': {'total_weight': 64253, 'runtime_in_sec': 45204.53, 'dimension': 2152}, 'u2319': {'total_weight': 234256, 'runtime_in_sec': 7067.93, 'dimension': 2319}, 'ulysses16': {'total_weight': 6859, 'runtime_in_sec': 0.22, 'dimension': 16}, 'ulysses22': {'total_weight': 7013, 'runtime_in_sec': 0.53, 'dimension': 22}, 'usa13509': {'total_weight': 19982859, 'runtime_in_sec': '~4 years', 'dimension': 13509}, 'vm1084': {'total_weight': 239297, 'runtime_in_sec': 604.78, 'dimension': 1084}, 'vm1748': {'total_weight': 336556, 'runtime_in_sec': 2223.65, 'dimension': 1748}
     }

TSPLIB_GROUPS = Literal[
    "0_to_125",         # number of nodes between 0 and 125
    "125_to_500",       # number of nodes between 125 and 500
    "500_to_5000",      # number of nodes between 500 and 5000
    "above_5000",       # number of nodes above 5000
    "integral_test"     # small (undirected), small (directed), mid-size (undirected)
]

def get_TSPLIB_Concorde_benchmark(name: str):
    # Check for solution computed by Concorde solver
    if name in TSPLIB_CONCORDE_BENCHMARKS.keys():
         return Benchmark(name="Concorde",
                          info="Performance of Concorde (03.12.19).",
                          total_weight=TSPLIB_CONCORDE_BENCHMARKS[name]["total_weight"],
                          runtime_in_sec=TSPLIB_CONCORDE_BENCHMARKS[name]["runtime_in_sec"]
                          )
    else:
        return None


def get_TSPLIB_instances(group: TSPLIB_GROUPS):
    # Select instances based on group name
    
    if group == "0_to_125":
        instance_names = [name for name, values in TSPLIB_CONCORDE_BENCHMARKS.items() if 0 < values["dimension"] <= 125]
    elif group == "125_to_500":
        instance_names = [name for name, values in TSPLIB_CONCORDE_BENCHMARKS["instances"].items() if 125 < values["dimension"] <= 500]
    elif group == "500_to_5000":
        instance_names = [name for name, values in TSPLIB_CONCORDE_BENCHMARKS["instances"].items() if 500 < values["dimension"] <= 5000]
    elif group == "above_5000":
        instance_names = [name for name, values in TSPLIB_CONCORDE_BENCHMARKS["instances"].items() if values["dimension"] > 5000]
    elif group == "integral_test":
        # Manually selected representative instances for integral testing
        instance_names = [
            "burma14",    # small, undirected
            "bays29",     # small, directed
            "u159",       # midsize, undirected
            # "dsj1000"     # large, undirected
        ]
    else:
        raise ValueError(f"TSPLIB instance group '{group}' not defined")
    
    return [create_instance_from_file(name=name, 
                                      benchmark=get_TSPLIB_Concorde_benchmark(name=name)) 
            for name in instance_names]


def barchart_gap_per_instance(df):
    fig = px.bar(df, x="instance", y="gap_to_benchmark_in_pct", color="solution_method", barmode='group',)

    fig.update_layout(width=1200, height=800, template="simple_white")    
    fig.show()


def boxplot_gap_per_method(df):
    fig = px.box(df, x="solution_method", y="gap_to_benchmark_in_pct")

    fig.update_layout(width=800, height=800, template="simple_white")
    fig.show()


# def load_results()


def solve_tsplib_instances(methods: list, group: TSPLIB_GROUPS, max_runtime_in_sec: int = 3) -> pd.DataFrame:
    """
    Solves selected TSPLIB instances using specified methods.

    :param methods: List of method names to use (e.g., ["nearest_neighbor", "pyVRP"] or ["all"])
    :param group: Name of the instance group to solve
    """
    
    instance_names = get_TSPLIB_instances(group=group)   

    results = []

    # Loop through each instance and apply selected methods
    for name in instance_names:
        
        my_tsp = create_instance_from_file(name=name, 
                                           benchmark=get_TSPLIB_Concorde_benchmark(name=name))

        for method in methods:
            try:
                if method == "nearest_neighbor" or method == "all":
                    my_tour = NearestNeighbor().solve(instance=my_tsp)

                if method == "christofidesx" or method == "all":
                    my_tour = Christofidesx().solve(instance=my_tsp)

                if method == "pyVRP" or method == "all":
                    my_tour = pyVRP(instance=my_tsp, max_runtime_in_sec=max_runtime_in_sec, display=False).solve()

                results.append(my_tour.info_for_export())

                # print(my_tour)
                my_tour.print_info()

            except Exception as error:
                print(f"An error occurred while solving {name} with {method}: {error}")

    return pd.DataFrame(results)


def do_experiment(list_of_solver: list, list_of_instances: list, 
                  export_to_file: str = None, import_previous_files: list = None):
    
    results = []
    for solver in list_of_solver:
        list_of_tours = solver.solve_multiple_instances(list_of_instances=list_of_instances)

        for tour in list_of_tours:
            if tour is not None:
                results.append(tour.info_for_df())
    
    df = pd.DataFrame(results)

    if import_previous_files is not None:
        df_list = []

        for file in import_previous_files:
            # Determine the root of the repository by going one level up from the current file
            repo_root = Path(__file__).resolve().parent
            file_name = file + ".xlsx"        
            path_to_file = repo_root / "Output" / file_name

            if path_to_file.exists():
                df_list.append(pd.read_excel(path_to_file))
            else:
                raise FileNotFoundError(f"Results file not found: /Output/{file}.xlsx")
    

        df_list.append(df)

        # Combine them into one big DataFrame
        df = pd.concat(df_list, ignore_index=True)

    if export_to_file is not None:
        # Determine the root of the repository by going one level up from the current file
        repo_root = Path(__file__).resolve().parent

        file_name = export_to_file + ".xlsx"        
        path_to_file = repo_root / "Output" / file_name

        df.to_excel(path_to_file, index=False)

    return df


if __name__ == "__main__":
    df = do_experiment(
        list_of_solver=[
            NearestNeighbor(),
            Christofidesx()
            # pyVRP(max_runtime_in_sec=3, display=False)
            ],
        list_of_instances=get_TSPLIB_instances(group="integral_test"), 
        export_to_file="integral_all", 
        import_previous_files=["integral_all"])

    # barchart_gap_per_instance(df)
    # boxplot_gap_per_method(df)

    print(df)