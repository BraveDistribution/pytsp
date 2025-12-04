# Import pyTSP structures
from pytsp.structures.Instance import Instance
from pytsp.structures.Tour import Tour


# Import other modules
from abc import ABC, abstractmethod
import logging

class SolutionMethod(ABC):
    """
    Abstract base class for TSP solution methods.

    Subclasses must implement:
        - solve(instance): Returns a Tour object for the given Instance.

    Provides:
        - print_all_attributes(): Prints all attributes except 'instance'.
        - solve_multiple_instances(): Solves a list of instances and returns their tours.
    """

    def __init__(self, name: str, info: str = None, logging_level: int = logging.WARNING):
        """
        Initialize the object with a name and optional info string.
        
        Parameters:
            name (str): Identifier for the instance.
            info (str, optional): Additional descriptive information. Defaults to None.
            logging_level (int): Controls verbosity of output. Levels: NOTSET(0), DEBUG(10), INFO(20), WARNING(30), ERROR(40), CRITICAL(50)
        """

        # Base initializer (can be extended by subclasses)
        self.name = name
        self.info = info

        # Configure logging
        logging.basicConfig(
            level=logging.WARNING,
            format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging_level)

    @abstractmethod
    def solve(self, instance: Instance) -> Tour:
        """
        Abstract method to solve a single TSP instance.

        Args:
            instance (Instance): The TSP instance to solve.

        Returns:
            Tour: The computed tour for the instance.
        """
        pass  # Must be implemented by subclasses
    

    def print_all_attributes(self):
        """
        Prints all attributes of the solver object except 'instance'.
        Useful for debugging or inspecting solver configuration.
        """
        for attr, value in self.__dict__.items():
            if attr != 'instance':
                print(f"{attr}: {value}")

    def solve_multiple_instances(self, list_of_instances: list):
        """
        Solves multiple TSP instances using the solver.

        Args:
            list_of_instances (list): A list of Instance objects to solve.

        Returns:
            list: A list of Tour objects corresponding to the solved instances.
        """
        list_of_tours = []

        # Iterate over each instance and solve it
        for instance in list_of_instances:
            self.logger.info(f"Solve instance {instance.name}")

            # Solve the instance and store the resulting tour
            my_tour = self.solve(instance=instance)
            list_of_tours.append(my_tour)

        return list_of_tours