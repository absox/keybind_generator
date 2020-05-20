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
                                  ["ice barrage", 1, "Yes", numpy.nan],
                                  ["dbreath", 2, "Yes", numpy.nan]])
        cls.abilities.columns = ["name", "priority", "bar", "comment"]

        cls.combinations = DataFrame([["ice barrage>wrack", 2, "Yes", "", [2, 0]],
                                     ["ice barrack>wrack #2", 2, "Yes", "", [2, 1]]])
        cls.combinations.columns = ["name", "priority", "ordered", "comment", "indices"]

    def test_key_binding_string_generation(self):
        key_binding = KeyBinding(self.graph, self.abilities, self.combinations, self.graph.get_node_indices(["a", "b"]))
        self.assertEqual(str(key_binding), "")

        key_binding.assign_next(0)
        self.assertEqual(str(key_binding), "wrack : a")

        key_binding.assign_next(1)
        self.assertEqual(str(key_binding), "wrack : a\nwrack #2 : b")

        key_binding.assign_next(2)

        key_binding.assign_next(3)

        print(key_binding)

    def test_key_binding_assignment(self):
        key_binding = KeyBinding(self.graph, self.abilities, self.combinations, self.graph.get_node_indices(["a", "b"]))

        self.assertTrue(numpy.array_equal(key_binding.get_unassigned(), range(5)))
        self.assertTrue(key_binding.assign_next(0))
        self.assertTrue(numpy.array_equal(key_binding.get_unassigned(), range(1, 5)))
        self.assertFalse(key_binding.fully_assigned())
        self.assertTrue(key_binding.assign_next(1))
        self.assertTrue(numpy.array_equal(key_binding.get_unassigned(), range(2, 5)))
        self.assertFalse(key_binding.fully_assigned())
        self.assertTrue(key_binding.assign_next(2))
        self.assertTrue(numpy.array_equal(key_binding.get_unassigned(), range(3, 5)))
        self.assertTrue(key_binding.assign_next(3))
        self.assertTrue(key_binding.fully_assigned())
        self.assertTrue(numpy.array_equal(key_binding.get_unassigned(), [4]))

        self.assertEqual(key_binding.get_assignment("wrack"), 0)
        self.assertEqual(key_binding.get_assignment("wrack #2"), 1)
        self.assertEqual(key_binding.get_assignment("ice barrage"), 2)
        self.assertEqual(key_binding.get_assignment("dbreath"), 3)

    def test_loss_function(self):
        key_binding = KeyBinding(self.graph, self.abilities, self.combinations, self.graph.get_node_indices(["a", "b"]))
        key_binding.assign_next(0)
        key_binding.assign_next(1)

        self.assertTrue(numpy.isnan(key_binding.eval_loss()))

        self.assertTrue(key_binding.assign_next(2))
        self.assertTrue(key_binding.assign_next(3))

        self.assertFalse(numpy.isnan(key_binding.eval_loss()))
        self.assertEqual(key_binding.eval_loss(), 3.5)


if __name__ == '__main__':
    unittest.main()
