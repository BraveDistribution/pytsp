# Importing pyTSP structures
from pytsp.structures.Instance import Instance
from pytsp.structures.SolutionMethod import SolutionMethod

# Importing other modules
import logging
import pandas as pd
import plotly.express as px
from time import time

# Info: For PDF export, kaleido needs to be in version 0.0.0post1 (pip install kaleido==0.1.0post1)

class Experiment:
    """
    Wrapper class for a TSP experiment.

    Provides convenient methods to analyze different solution methods across different instances. 
    """

    def __init__(self, name, list_of_instances: list = None, list_of_solution_methods: list = None, logging_level: int = logging.INFO):
        """
        Initialize the object with a name, a list of problem instances, and a list of solution methods.

        Parameters
        ----------
        name (str): The name of the object or experiment.
        list_of_instances (list, optional): A list of problem instances (default is an empty list).
        list_of_solution_methods (list, optional): A list of solution methods (default is an empty list).
        logging_level (int): Controls verbosity of output. Levels: NOTSET(0), DEBUG(10), INFO(20), WARNING(30), ERROR(40), CRITICAL(50)
        """
        self.name = name  # Name of the experiment or object

        # Initialize the list of instances; use empty list if None is provided
        self.list_of_instances = [] if list_of_instances is None else list_of_instances

        # Initialize the list of solution methods; use empty list if None is provided
        self.list_of_solution_methods = [] if list_of_solution_methods is None else list_of_solution_methods

        self.df_results = None  # Placeholder for results DataFrame


        # Configure logging
        logging.basicConfig(
            level=logging.WARNING,
            format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging_level)

    def add_instance(self, instance: Instance):
        """
        Add a problem instance to the list of instances.

        Parameters
        ----------
        instance : Instance
            A TSP problem instance to be added.
        """
        self.instances.append(instance)  # Append the instance to the list


    def add_method(self, method: SolutionMethod):
        """
        Add a solution method to the list of methods.

        Parameters
        ----------
        method : SolutionMethod
            A method used to solve TSP instances.
        """
        self.methods.append(method)  # Append the method to the list

    def run(self):
        """
        Run the experiment by solving multiple TSP instances using the specified solution methods.
        Collects results from each run and stores them in the class's results DataFrame.

        """
        self.logger.info(
            f"Experiment: '{self.name}' with "
            f"{len(self.list_of_instances)} instances and "
            f"{len(self.list_of_solution_methods)} solution methods."
        )

        # Initialize a list to store results from each tour
        results = []

        # Iterate over each solution method
        for solution_method in self.list_of_solution_methods:


            # Start timing the method execution
            start_time = time()

            # Print the name of the current solver
            self.logger.info(f"{solution_method.name}: Start")

            # Solve all instances using the current method
            list_of_tours = solution_method.solve_multiple_instances(list_of_instances=self.list_of_instances)

            # Collect result information from each tour
            for tour in list_of_tours:
                if tour is not None:
                    # Append tour info as a dictionary for DataFrame creation
                    results.append(tour.info_for_df())

            # Print completion message with runtime
            self.logger.info(f"{solution_method.name}: Completed in {round(time() - start_time, 4)} seconds.")

        # Convert the list of dictionaries into a pandas DataFrame
        df_new_results = pd.DataFrame(results)

        # Merge with existing results if present
        if self.df_results is None:
            self.df_results = df_new_results
        else:
            self.df_results = pd.concat([self.df_results, df_new_results], ignore_index=True)

    def load_results(self, path_to_df_files: list):
        """
        Load and merge result DataFrames from a list of file paths.
        Each file is expected to contain a pandas DataFrame with the columns as specified in the Tour.info_for_df() method. 

        Parameters
        ----------
        path_to_df_files : list
            A list of pathlib.Path objects pointing to Excel files containing result DataFrames.

        Raises
        ------
        FileNotFoundError
            If any of the specified files do not exist.
        """
        # Start with existing results if available
        df_list = [] if self.df_results is None else [self.df_results]

        # Iterate over each provided file path
        for path_to_df in path_to_df_files:
            if path_to_df.exists():
                # Read the Excel file into a DataFrame and append to the list
                df_list.append(pd.read_excel(path_to_df))
            else:
                # Raise an error if the file is not found
                raise FileNotFoundError(f"Experiment: Results file not found: {path_to_df}")

        # Concatenate all DataFrames into a single DataFrame
        self.df_results = pd.concat(df_list, ignore_index=True)

    def export_results(self, path_to_file: str):
        """
        Export the results DataFrame to an Excel file.

        Parameters
        ----------
        path_to_file : str
            The file path where the Excel file should be saved.
        """
        # Save the results DataFrame to the specified Excel file
        self.df_results.to_excel(path_to_file, index=False)

    def get_barchart_gap_per_instance(self):
        """
        Create a grouped bar chart showing the gap to benchmark for each instance,
        grouped by solution method.

        Returns
        -------
        plotly.graph_objs._figure.Figure
            A Plotly Figure object representing the grouped bar chart.
        """
        # Create a grouped bar chart using Plotly Express
        fig = px.bar(
            self.df_results,
            x="instance",                      # X-axis: instance names
            y="gap_to_benchmark_in_pct",       # Y-axis: gap percentage compared to benchmark
            color="solution_method",           # Different colors for each solution method
            barmode="group"                    # Group bars by instance
        )

        # Update layout for better visualization
        fig.update_layout(
            width=1200,                        # Set chart width
            height=800,                        # Set chart height
            template="simple_white"            # Use a clean white template
        )

        return fig

    def get_boxplot_gap_per_method(self):
        """
        Create a box plot showing the distribution of gap percentages for each solution method.

        Returns
        -------
        plotly.graph_objs._figure.Figure
            A Plotly Figure object representing the box plot.
        """
        # Create a box plot using Plotly Express
        fig = px.box(
            self.df_results,
            x="solution_method",               # X-axis: solution methods
            y="gap_to_benchmark_in_pct"        # Y-axis: gap percentage compared to benchmark
        )

        # Update layout for better visualization
        fig.update_layout(
            width=800,                         # Set chart width
            height=800,                        # Set chart height
            template="simple_white"            # Use a clean white template
        )

        return fig