import unittest

import numpy
from pandas import DataFrame

from keybind_generator.util.Graph import Graph
from keybind_generator.util.KeyBinding import KeyBinding


class TestKeyBinding(unittest.TestCase):
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
                                  ["wrack #3", 1, "Yes", numpy.nan],
                                  ["dbreath", 2, "Yes", numpy.nan]])

        cls.combinations = DataFrame([["wrack>wrack #2", 1, "Yes", ""],
                                     ["wrack #2>wrack #3", 1, "Yes", ""]])

    def test_key_binding_assignment(self):

        key_binding = KeyBinding(self.graph, self.abilities, self.combinations, self.graph.get_node_indices(["a", "b"]))

    def test_loss_function(self):
        # TODO
        pass


if __name__ == '__main__':
    unittest.main()
