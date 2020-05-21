import unittest
import numpy
from pandas import DataFrame

from keybind_generator.data.SpreadsheetReader import SpreadsheetReader
from keybind_generator.util.Graph import Graph
from test import base_dir


class TestGraph(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.graph = Graph(5, ["a", "b", "c", "d", "e"])
        cls.graph.adjacency = numpy.array([[0, 1.5, 2.5, 3.5, 4.5],
                                       [1.5, 0, 1, 2, 3],
                                       [2.5, 1, 0, 2, 2],
                                       [3.5, 2, 2, 0, 2],
                                       [4.5, 3, 2, 2, 0]])

    def test_minimum_distance(self):
        self.assertEqual(self.graph.minimum_distance(0, 1), 1.5)
        self.assertEqual(self.graph.minimum_distance(0, [2, 3]), 2.5)
        self.assertEqual(self.graph.minimum_distance([0, 1], [1, 2]), 0)
        self.assertEqual(self.graph.minimum_distance([0, 1], [2, 3]), 1)

    def test_path_length(self):
        self.assertEqual(self.graph.path_length([0, 1, 2]), 2.5)


if __name__ == '__main__':
    unittest.main()
