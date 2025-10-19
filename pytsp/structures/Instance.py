import tsplib95
from typing import Literal
from pyparsing import Path
from TSP.Benchmark import Benchmark
from TSP import Tour

import plotly.express as px
import pandas as pd

EdgeWeightType = Literal[
    "EXPLICIT",  # Weights are listed explicitly in the corresponding section
    "EUC_2D",    # Weights are Euclidean distances in 2-D
    "EUC_3D",    # Weights are Euclidean distances in 3-D
    "MAX_2D",    # Weights are maximum distances in 2-D
    "MAX_3D",    # Weights are maximum distances in 3-D
    "MAN_2D",    # Weights are Manhattan distances in 2-D
    "MAN_3D",    # Weights are Manhattan distances in 3-D
    "CEIL_2D",   # Weights are Euclidean distances in 2-D rounded up
    "GEO",       # Weights are geographical distances
    "ATT",       # Special distance function for problems att48 and att532
    "XRAY1",     # Special distance function for crystallography problems (Version 1)
    "XRAY2",     # Special distance function for crystallography problems (Version 2)
    "SPECIAL"    # There is a special distance function documented elsewhere
]


EdgeWeightFormat = Literal[
    "FUNCTION",          # Weights are given by a function
    "FULL_MATRIX",       # Weights are given by a full matrix
    "UPPER_ROW",         # Upper triangular matrix (row-wise without diagonal entries)
    "LOWER_ROW",         # Lower triangular matrix (row-wise without diagonal entries)
    "UPPER_DIAG_ROW",    # Upper triangular matrix (row-wise including diagonal entries)
    "LOWER_DIAG_ROW",    # Lower triangular matrix (row-wise including diagonal entries)
    "UPPER_COL",         # Upper triangular matrix (column-wise without diagonal entries)
    "LOWER_COL",         # Lower triangular matrix (column-wise without diagonal entries)
    "UPPER_DIAG_COL",    # Upper triangular matrix (column-wise including diagonal entries)
    "LOWER_DIAG_COL"     # Lower triangular matrix (column-wise including diagonal entries)
]


DisplayDataType = Literal[
    "COORD_DISPLAY",  # Display is generated from the node coordinates
    "TWOD_DISPLAY",   # Explicit coordinates in 2-D are given
    "NO_DISPLAY"      # No graphical display is possible
]


def create_instance_from_file(name: str, benchmark: Benchmark = None):
    """
    Loads a TSPLIB-formatted TSP instance from a file.

    Parameters:
        name (str): The name of the TSPLIB instance file (without extension).

    Returns:
        Instance: A parsed TSP instance object.
    
    Raises:
        FileNotFoundError: If the specified .tsp file does not exist.
    """
    # Determine the root of the repository by going one level up from the current file
    repo_root = Path(__file__).resolve().parent.parent

    # Construct the full path to the .tsp file
    file_name = name + ".tsp"
    path_to_file = repo_root / "DefaultInstances" / "TSPLIB" / file_name

    # Print the path for debugging purposes
    # print(path_to_file)

    # Raise an error if the file does not exist
    if not path_to_file.is_file():
        raise FileNotFoundError(f"TSPLIB file not found: {path_to_file}")

    # Load and return the TSP instance using tsplib95
    return Instance(TSPLIB=tsplib95.load(path_to_file), 
                    benchmark=benchmark)


def create_instance_from_coordinates(
    name: str,
    coordinates: list,
    comment: str = None,
    edge_weight_type: EdgeWeightType = "GEO",
    edge_weight_format: EdgeWeightFormat = "FUNCTION",
    display_data_type: DisplayDataType = "COORD_DISPLAY"
):
    """
    Creates a TSPLIB-formatted TSP instance from a list of coordinates.

    Args:
        name (str): Name of the TSP instance.
        coordinates (list): List of (x, y) tuples representing node coordinates.
        comment (str, optional): Optional comment describing the instance.
        edge_weight_type (EdgeWeightType, optional): Method used to calculate edge weights (default is GEO).
        edge_weight_format (EdgeWeightFormat, optional): Format of edge weights if explicit (default is FUNCTION).
        display_data_type (DisplayDataType, optional): Display type for graphical visualization (default is COORD_DISPLAY).

    Returns:
        Instance: A parsed TSPLIB instance using tsplib95.
    """

    # Build the TSPLIB header with metadata and configuration
    text = f"""NAME: {name}
TYPE: TSP
COMMENT: {comment}
DIMENSION: {len(coordinates)}
EDGE_WEIGHT_TYPE: {edge_weight_type}
EDGE_WEIGHT_FORMAT: {edge_weight_format} 
DISPLAY_DATA_TYPE: {display_data_type}
NODE_COORD_SECTION"""

    # Append each coordinate with its node index (1-based)
    for idx, c in enumerate(coordinates):
        text += f"""
   {idx + 1}   {c[0]}   {c[1]}"""

    # Mark the end of the TSPLIB file
    text += """
EOF
"""

    # Parse the TSPLIB-formatted string and return the instance
    return Instance(tsplib95.parse(text))


def create_instance_from_cost_matrix(
    name: str,
    cost_matrix: list,
    comment: str = None,
    edge_weight_type: EdgeWeightType = "EXPLICIT",
    edge_weight_format: EdgeWeightFormat = "FULL_MATRIX",
    display_data_type: DisplayDataType = "NO_DISPLAY",
    display_coordinates: list = None
):
    """
    Creates a TSPLIB-formatted TSP instance from a cost matrix.

    Args:
        name (str): Name of the TSP instance.
        cost_matrix (list): 2D list representing the cost/distance matrix.
        comment (str, optional): Optional comment describing the instance.
        edge_weight_type (EdgeWeightType, optional): Type of edge weights (default is EXPLICIT).
        edge_weight_format (EdgeWeightFormat, optional): Format of edge weights (default is FULL_MATRIX).
        display_data_type (DisplayDataType, optional): Optional display type for graphical visualization.
        display_coordinates (list, optional): Optional list of (x, y) coordinates for display.

    Returns:
        Instance: A parsed TSPLIB instance using tsplib95.
    """

    # Build the TSPLIB header with metadata and configuration
    text = f"""NAME: {name}
TYPE: TSP
COMMENT: {comment}
DIMENSION: {len(cost_matrix[0])}
EDGE_WEIGHT_TYPE: {edge_weight_type}
EDGE_WEIGHT_FORMAT: {edge_weight_format}"""

    # Optionally include display data type if provided
    if display_data_type is not None:
        text += f"""
DISPLAY_DATA_TYPE: {display_data_type}"""

    # Add the edge weight section with the cost matrix values
    text += f"""
EDGE_WEIGHT_SECTION"""

    for row in cost_matrix:
        text += "\n"
        for cost in row:
            text += " " + str(cost)

    # Add display coordinates if provided
    if display_coordinates:
        text += """
DISPLAY_DATA_SECTION"""
        for idx, c in enumerate(display_coordinates):
            text += f"""
   {idx + 1}   {c[0]}   {c[1]}"""

    # Mark the end of the TSPLIB file
    text += """
EOF
"""

    # Parse the TSPLIB-formatted string and return the instance
    return Instance(tsplib95.parse(text))


class Instance:
    """
    Wrapper class for a TSP instance (based on TSPLIB95 logic).

    Provides convenient access to nodes, edges, and weight-related utilities.
    """

    def __init__(self, TSPLIB, benchmark: Benchmark = None):
        """
        Initializes the Instance with a parsed TSPLIB object.

        Args:
            TSPLIB: A parsed TSPLIB95 instance.
        """
        self.TSPLIB = TSPLIB
        self.name = self.TSPLIB.name
        self.benchmark = benchmark

        # Extract the list of nodes and edges from the TSPLIB instance
        self.nodes = list(self.TSPLIB.get_nodes())
        self.edges = list(self.TSPLIB.get_edges())

        # networkx_graph = TSPLIB.get_graph()
        # print(networkx_graph)
        # print(networkx_graph.nodes)
        # print(networkx_graph.edges)

        # Compute number of stops/nodes
        self.number_of_stops = len(self.nodes)

        # Try to get node coordinates from TSPLIB data
        if 'node_coords' in self.TSPLIB.as_name_dict():
            self.node_coords = self.TSPLIB.node_coords
        elif 'display_data' in self.TSPLIB.as_name_dict() and self.TSPLIB.display_data_type == "TWOD_DISPLAY":
            self.node_coords = self.TSPLIB.display_data
        else:
            self.node_coords = None            
        
    def get_weight(self, source, target):
        """
        Returns the weight (distance or cost) between two nodes.

        Args:
            source: The source node ID.
            target: The target node ID.

        Returns:
            The weight between source and target.
        """
        return self.TSPLIB.get_weight(source, target)

    def get_full_cost_matrix(self):
        """
        Constructs and returns the full cost matrix of the TSP instance.

        Returns:
            A 2D list representing the cost matrix.
        """
        cost_matrix = []

        # Iterate over all node pairs to compute weights
        for source in self.nodes:
            cost_matrix_row = []
            for target in self.nodes:
                cost_matrix_row.append(self.get_weight(source, target))
            cost_matrix.append(cost_matrix_row)

        return cost_matrix

    def get_info(self):
        """
        Return a short description of the TSP instance.

        Returns:
            str: A string describing the number of nodes and edges.
        """
        return f"TSP {self.name} with {len(self.nodes)} nodes and {len(self.edges)} edges."
           
    def plot(self, tour: Tour = None):
        """
        Plot the TSP instance or a given tour.

        Args:
            tour (Tour, optional): A Tour object to visualize. If None, only the nodes are plotted.
        """
        # Exit if instance does not include node coordinates
        if self.node_coords is None:
            print("Error: Plotting failed because no node coordinates were provided.")
            return

        # Plot only the nodes if no tour is provided
        if tour is None:
            x_values = [v[0] for v in self.node_coords.values()]
            y_values = [v[1] for v in self.node_coords.values()]

            df = pd.DataFrame(dict(x=x_values, y=y_values))

            fig = px.scatter(df, x="x", y="y", title=f"Instance: {self.get_info()}")
        else:
            # Plot the tour path including return to the start
            x_values, y_values = zip(*(self.node_coords[n] for n in tour.sequence + [tour.sequence[0]]))

            df = pd.DataFrame(dict(x=x_values, y=y_values))

            fig = px.line(df, x="x", y="y", markers=True, title=str(tour))
            fig.update_traces(line={'color': 'black'})

        # Final plot formatting
        fig.update_layout(width=1200, height=1200, template="simple_white")
        fig.update_traces(marker={'size': 10, 'color': 'black'})
        fig.show()
