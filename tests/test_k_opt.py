import numpy as np

from pytsp import k_opt_tsp
from pytsp.data_structures.opt_case import OptCase
from pytsp.k_opt_tsp import reverse_segments, tsp_3_opt, tsp_2_opt, get_solution_cost_change
from pytsp.utils import route_cost


class TestKOpt():
    A = [0, 1]
    B = [2, 3]
    C = [4, 5]

    graph = np.array([[0, 7, 6, 3, 1, 2],
                      [7, 0, 9, 3, 4, 2],
                      [6, 9, 0, 3, 6, 7],
                      [3, 3, 3, 0, 2, 5],
                      [1, 4, 6, 2, 0, 1],
                      [2, 2, 7, 5, 1, 0]])

    graph2 = np.array([[0, 4, 3, 4, 5, 1, 2, 3, 4],
                       [4, 0, 1, 4, 3, 4, 6, 2, 1],
                       [3, 1, 0, 1, 4, 3, 2, 1, 9],
                       [4, 4, 1, 0, 4, 6, 1, 2, 3],
                       [5, 3, 4, 4, 0, 1, 2, 5, 3],
                       [1, 4, 3, 6, 1, 0, 2, 5, 3],
                       [2, 6, 2, 1, 2, 2, 0, 3, 5],
                       [3, 2, 1, 2, 5, 5, 3, 0, 9],
                       [4, 1, 9, 3, 3, 3, 5, 9, 0]
                       ])

    def test_get_all_segments(self):
        segments = k_opt_tsp.possible_segments(6)
        assert [(0, 2, 4), (1, 3, 5)] == list(segments)

    def test_get_all_segments2(self):
        segments = k_opt_tsp.possible_segments(7)
        assert [(1, 3, 5), (1, 3, 6), (1, 4, 6), (2, 4, 6), (2, 4, 7), (2, 5, 7), (3, 5, 7)] == list(segments)

    def test_reverse_segment_case1(self):
        route = [0, 1, 2, 3, 4, 5]
        i, j, k = 1, 3, 5
        result = reverse_segments(route, OptCase.opt_case_1, i, j, k)
        assert result == self.A + self.B + self.C

        result = reverse_segments(route, OptCase.opt_case_2, i, j, k)
        assert result == self.A + self.B + list(reversed(self.C))

        result = reverse_segments(route, OptCase.opt_case_3, i, j, k)
        assert result == self.A + list(reversed(self.B)) + self.C

        result = reverse_segments(route, OptCase.opt_case_4, i, j, k)
        assert result == self.A + list(reversed(self.B)) + list(reversed(self.C))

        result = reverse_segments(route, OptCase.opt_case_5, i, j, k)
        assert result == self.A + self.C + list(reversed(self.B))

        result = reverse_segments(route, OptCase.opt_case_6, i, j, k)
        assert result == self.A + list(reversed(self.C)) + list(reversed(self.B))

        result = reverse_segments(route, OptCase.opt_case_7, i, j, k)
        assert result == self.A + list(reversed(self.C)) + self.B

        result = reverse_segments(route, OptCase.opt_case_8, i, j, k)
        assert result == self.A + self.C + self.B

    def test_3_opt_algorithm(self):
        graph = np.array([[0, 5, 2, 1, 1, 4],
                          [5, 0, 6, 2, 2, 5],
                          [2, 6, 0, 7, 4, 2],
                          [1, 2, 7, 0, 8, 4],
                          [1, 2, 4, 8, 0, 5],
                          [4, 5, 2, 4, 5, 0]])
        route = [0, 1, 2, 3, 4, 5]
        result = tsp_3_opt(graph, route)
        new_route_cost = route_cost(graph, result)
        old_route_cost = route_cost(graph, route)
        print(new_route_cost)
        print(result)
        print(old_route_cost)
        assert old_route_cost > new_route_cost

    def test_2_opt_algorithm(self):
        graph = np.array([[0, 5, 2, 1, 1, 4],
                          [5, 0, 6, 2, 2, 5],
                          [2, 6, 0, 7, 4, 2],
                          [1, 2, 7, 0, 8, 4],
                          [1, 2, 4, 8, 0, 5],
                          [4, 5, 2, 4, 5, 0]])
        route = [0, 1, 2, 3, 4, 5]
        result = tsp_2_opt(graph, route)
        new_route_cost = route_cost(graph, result)
        old_route_cost = route_cost(graph, route)
        print(new_route_cost)
        print(old_route_cost)
        print(result)
        assert old_route_cost > new_route_cost

    def test_get_solution_cost_change(self):
        graph = np.array([[0, 5, 2, 1, 1, 4],
                          [5, 0, 6, 2, 2, 5],
                          [2, 6, 0, 7, 4, 2],
                          [1, 2, 7, 0, 8, 4],
                          [1, 2, 4, 8, 0, 5],
                          [4, 5, 2, 4, 5, 0]])
        route = [0, 1, 2, 3, 4, 5]
        result = get_solution_cost_change(graph, route, OptCase.opt_case_1, 1, 3, 5)
        assert result == 0

        result = get_solution_cost_change(graph, route, OptCase.opt_case_2, 1, 3, 5)
        assert result == 7

        result = get_solution_cost_change(graph, route, OptCase.opt_case_3, 1, 3, 5)
        assert result == 8

        result = get_solution_cost_change(graph, route, OptCase.opt_case_4, 1, 3, 5)
        assert result == 13

        result = get_solution_cost_change(graph, route, OptCase.opt_case_5, 1, 3, 5)
        assert result == 10

        result = get_solution_cost_change(graph, route, OptCase.opt_case_6, 1, 3, 5)
        assert result == 3

        result = get_solution_cost_change(graph, route, OptCase.opt_case_7, 1, 3, 5)
        assert result == 8

        result = get_solution_cost_change(graph, route, OptCase.opt_case_8, 1, 3, 5)
        assert result == 13

    def test_2_opt_2(self):
        route = [0, 3, 2, 1, 4, 5, 6, 7, 8]
        result = tsp_2_opt(self.graph2, route)
        new_route_cost = route_cost(self.graph2, result)
        old_route_cost = route_cost(self.graph2, route)
        print(new_route_cost)
        print(old_route_cost)
        assert new_route_cost < old_route_cost

    def test_3_opt_2(self):
        route = [0, 3, 2, 1, 4, 5, 6, 7, 8]
        result = tsp_3_opt(self.graph2, route)
        new_route_cost = route_cost(self.graph2, result)
        old_route_cost = route_cost(self.graph2, route)
        print(new_route_cost)
        print(old_route_cost)
        assert new_route_cost < old_route_cost
