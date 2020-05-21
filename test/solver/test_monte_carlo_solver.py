import unittest

import numpy
from pandas import DataFrame

from keybind_generator.solver.MonteCarloTreeSearchSolver import MonteCarloTreeSearchSolver
from keybind_generator.util.Graph import Graph


class TestMonteCarloSolver(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = Graph(5, ["a", "b", "c", "d", "e"])
        cls.graph.adjacency = numpy.array([[0, 1, 2, 3, 4],
                                           [1, 0, 1, 2, 3],
                                           [2, 1, 0, 1, 2],
                                           [3, 2, 1, 0, 1],
                                           [4, 3, 2, 1, 0]])

        cls.abilities = DataFrame([["wrack", 1, "Yes", numpy.nan],
                                   ["wrack #2", 1, "Yes", numpy.nan],
                                   ["ice barrage", 2, "Yes", numpy.nan],
                                   ["dbreath", 3, "Yes", numpy.nan]])
        cls.abilities.columns = ["name", "priority", "bar", "comment"]

        cls.combinations = DataFrame([["ice barrage>wrack", 1, "Yes", "", [2, 0]],
                                      ["ice barrack>wrack #2", 1, "Yes", "", [2, 1]]])
        cls.combinations.columns = ["name", "priority", "ordered", "comment", "indices"]

        cls.home_nodes = cls.graph.get_node_indices(["a", "b"])

    def test_mcts_solver(self):
        mcts_solver = MonteCarloTreeSearchSolver(self.graph, self.abilities, self.combinations, self.home_nodes)
        mcts_solver.do_num_iter(100)

        print(mcts_solver.best_loss)
        print(mcts_solver.best_binding)

        for child in mcts_solver.root.children:
            print(f"%d %f" % (child.visits, child.loss))



if __name__ == '__main__':
    unittest.main()
