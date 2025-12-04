import tsplib95

from pyparsing import Path
from .utils import EdgeWeightType, EdgeWeightFormat, DisplayDataType
from pytsp.structures.Benchmark import Benchmark
from pytsp.structures.Node import Node, Node2D
# from pytsp.structures.Tour import Tour

import plotly.express as px
import pandas as pd


def create_instance_from_file(name: str, benchmark: Benchmark = None):
    """
    Loads a TSPLIB-formatted TSP instance from a file.

    Parameters:
        name (str): The name of the TSPLIB instance file (without extension).
        benchmark (Benchmark): A benchmark object to be added to the new instance.

    Returns:
        Instance: A parsed TSP instance object.
    
    Raises:
        FileNotFoundError: If the specified .tsp file does not exist.
    """
    # Determine the root of the repository by going one level up from the current file
    repo_root = Path(__file__).resolve().parent.parent.parent

    # Construct the full path to the .tsp file
    file_name = name + ".tsp"
    path_to_file = repo_root / "pytsp" / "data" / "TSPLIB" / file_name

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
    display_data_type: DisplayDataType = "COORD_DISPLAY",
    benchmark: Benchmark = None
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
        benchmark (Benchmark): A benchmark object to be added to the new instance.

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
    return Instance(TSPLIB=tsplib95.parse(text), 
                    benchmark=benchmark)


def create_instance_from_cost_matrix(
    name: str,
    cost_matrix: list,
    comment: str = None,
    edge_weight_type: EdgeWeightType = "EXPLICIT",
    edge_weight_format: EdgeWeightFormat = "FULL_MATRIX",
    display_data_type: DisplayDataType = "NO_DISPLAY",
    display_coordinates: list = None,
    benchmark: Benchmark = None
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
        benchmark (Benchmark): A benchmark object to be added to the new instance.

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
    return Instance(TSPLIB=tsplib95.parse(text), 
                    benchmark=benchmark)


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
            benchmark (Benchmark): A benchmark object to be added to the new instance.
        """
        # Set TSPLIB instance
        self.TSPLIB = TSPLIB

        # Set benchmark 
        self.benchmark = benchmark
        
        # Set name from TSPLIB instance
        self.name = self.TSPLIB.name

        # Get nodes from TSPLIB data (if available, add coordinates)
        if 'node_coords' in self.TSPLIB.as_name_dict():
            self.nodes = [Node2D(id=n, x=self.TSPLIB.node_coords[n][0], y=self.TSPLIB.node_coords[n][1]) 
                          for n in self.TSPLIB.get_nodes()]
        elif 'display_data' in self.TSPLIB.as_name_dict() and self.TSPLIB.display_data_type == "TWOD_DISPLAY":
            self.nodes = [Node2D(id=n, x=self.TSPLIB.display_data[n][0], y=self.TSPLIB.display_data[n][1]) 
                          for n in self.TSPLIB.get_nodes()]
        else:
            self.nodes = [Node(id=n) for n in self.TSPLIB.get_nodes()]

        # Compute number of stops/nodes
        self.number_of_stops = len(self.nodes)
        
    def get_weight(self, source, target):
        """
        Retrieve the weight (distance or cost) between two nodes.

        Args:
            source (int): The source node.
            target (int): The target node.

        Returns:
            float: The weight between the source and target nodes.

        Raises:
            Exception: If the weight cannot be retrieved due to invalid node IDs or internal errors.
        """
        try:
            return self.TSPLIB.get_weight(source.id, target.id)
        except Exception as e:
            print(f"Error: Unable to retrieve weight between source={source} and target={target}. Please ensure that node IDs are correctly defined. Exception: {e}")
            raise
        
    def get_weight_via_id(self, source_id, target_id):
        """
        Retrieve the weight (distance or cost) between two nodes.

        Args:
            source (int): The source node ID.
            target (int): The target node ID.

        Returns:
            float: The weight between the source and target nodes.

        Raises:
            Exception: If the weight cannot be retrieved due to invalid node IDs or internal errors.
        """
        try:
            return self.TSPLIB.get_weight(source_id, target_id)
        except Exception as e:
            print(f"Error: Unable to retrieve weight between source={source_id} and target={target_id}. Please ensure that node IDs are correctly defined. Exception: {e}")
            raise
        
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
        return f"TSP {self.name} with {len(self.nodes)} nodes."

    def __str__(self):
        """
        The display string when printing the object

        :return: the display string
        :rtype: str
        """
        return f"Instance: {self.name}"

    def plot(self, tour: "Tour" = None):
        """
        Plot the TSP instance or a given tour.

        Args:
            tour (Tour, optional): A Tour object to visualize. If None, only the nodes are plotted.
        
        Returns
        -------
        plotly.graph_objs._figure.Figure
            A Plotly Figure object representing the box plot.
        """

        # Exit if instance does not include node coordinates
        if not isinstance(self.nodes[0], Node2D):
            print("Error: Plotting failed because no node coordinates were provided.")
            return None
        
        # Retrieve node coordinates
        node_coords = {n.id: (n.x, n.y) for n in self.nodes}

        if tour is None:
            # Plot only the nodes if no tour is provided
            x_values = [v[0] for v in node_coords.values()]
            y_values = [v[1] for v in node_coords.values()]

            df = pd.DataFrame(dict(x=x_values, y=y_values))

            fig = px.scatter(df, x="x", y="y", title=f"Instance: {self.get_info()}")
        else:
            # Plot the tour path including return to the start
            x_values, y_values = zip(*(node_coords[n.id] for n in tour.sequence + [tour.sequence[0]]))

            df = pd.DataFrame(dict(x=x_values, y=y_values))

            fig = px.line(df, x="x", y="y", markers=True, title=str(tour))
            fig.update_traces(line={'color': 'black'})

        # Final plot formatting
        fig.update_layout(width=1200, height=1200, template="simple_white")
        fig.update_traces(marker={'size': 10, 'color': 'black'})
        
        # Return figure
        return fig
