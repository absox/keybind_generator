import unittest

import numpy
from pandas import DataFrame

from keybind_generator.data.SpreadsheetReader import SpreadsheetReader
from keybind_generator.solver.PepegaSolver import PepegaSolver
from keybind_generator.util.Graph import Graph
from test import base_dir


class TestPepegaSolver(unittest.TestCase):

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
                                   ["dbreath", 2, "Yes", numpy.nan]])
        cls.abilities.columns = ["name", "priority", "bar", "comment"]

        cls.combinations = DataFrame([["ice barrage>wrack", 1, "Yes", "", [2, 0]],
                                      ["ice barrack>wrack #2", 1, "Yes", "", [2, 1]]])
        cls.combinations.columns = ["name", "priority", "ordered", "comment", "indices"]

        cls.home_nodes = cls.graph.get_node_indices(["a", "b"])

    def test_random_solver(self):
        pepega = PepegaSolver(self.graph, self.abilities, self.combinations, self.home_nodes)
        pepega.do_num_iter(1000)

        print(f"Loss: %f" % pepega.best_loss)
        print(pepega.best_binding)




if __name__ == '__main__':
    unittest.main()
