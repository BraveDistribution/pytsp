from abc import ABC, abstractmethod
from TSP import Instance
from TSP import Tour

class SolutionMethod(ABC):

    def __init__(self):
        pass
    
    @abstractmethod
    def solve(self, instance: Instance) -> Tour:
        pass  # This function must be implemented by any subclass

    def print_all_attributes(self):
        for attr, value in self.__dict__.items():
            if attr not in ['instance']:
                print(f"{attr}: {value}")

    def solve_multiple_instances(self, list_of_instances: list):
        list_of_tours = []

        for instance in list_of_instances:
            my_tour = self.solve(instance=instance)
            list_of_tours.append(my_tour)
        
        return list_of_tours

