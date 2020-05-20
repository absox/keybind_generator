import unittest

from keybind_generator.util.Keyboard import Keyboard


class TestKeyboard(unittest.TestCase):
    def test_keyboard_graph_generation_simple(self):
        keyboard = Keyboard()
        keyboard.add_key_row(Keyboard.KeyRow(1.5, 1, ["1", "2", "3", "4", "5", "6", "7", "8"]))
        keyboard.add_key_row(Keyboard.KeyRow(2.5, 1.2, ["Q", "W", "E", "R", "T", "Y"]))
        keyboard.add_key_row(Keyboard.KeyRow(3.5, 1.5, ["A", "S", "D", "F", "G", "H"]))
        keyboard.add_key_row(Keyboard.KeyRow(4.5, 2, ["Z", "X", "C", "V", "B", "N"]))
        graph = keyboard.generate_graph()

        self.assertEqual(graph.adjacency[0, 0], 0)
        self.assertEqual(graph.adjacency[0, 1], 1)
        self.assertEqual(graph.adjacency[0, 2], 2)
        self.assertEqual(graph.adjacency[0, 3], 3)

    def test_keyboard_graph_generation_modifier_penalty(self):
        keyboard = Keyboard()
        keyboard.add_key_row(Keyboard.KeyRow(1.5, 1, ["1", "2", "3", "4", "5", "6", "7", "8"]))
        keyboard.add_key_row(Keyboard.KeyRow(1.5, 1, ["1", "2", "3", "4", "5", "6", "7", "8"]), modifier="Shift",
                             modifier_penalty=4)
        graph = keyboard.generate_graph()

        self.assertEqual(graph.adjacency[0, 0], 0)
        self.assertEqual(graph.adjacency[0, 1], 1)
        self.assertEqual(graph.adjacency[0, 2], 2)
        self.assertEqual(graph.adjacency[0, 3], 3)

        self.assertEqual(graph.adjacency[0, 8], 4)
        self.assertEqual(graph.adjacency[0, 9], 5)
        self.assertEqual(graph.adjacency[0, 10], 6)
        self.assertEqual(graph.adjacency[0, 11], 7)

    def test_graph_generation_mouse(self):
        keyboard = Keyboard()
        keyboard.add_mouse_keys(["Mouse1", "Mouse2", "Mouse3"], mouse_penalty=4)

        graph = keyboard.generate_graph()

        self.assertEqual(graph.adjacency[0, 0], 0)
        self.assertEqual(graph.adjacency[0, 1], 8)  # Remember that expected penalty is the sum of the two
        self.assertEqual(graph.adjacency[1, 0], 8)

    def test_keyboard_graph_generation_mouse_keyboard_mixed(self):
        keyboard = Keyboard()
        keyboard.add_key_row(Keyboard.KeyRow(1.5, 1, ["1", "2", "3", "4", "5", "6", "7", "8"]))
        keyboard.add_mouse_keys(["Mouse1", "Mouse2", "Mouse3"], mouse_penalty=4)
        graph = keyboard.generate_graph()

        self.assertEqual(graph.adjacency[0, 9], 0)
        self.assertEqual(graph.adjacency[0, 10], 0)

        self.assertEqual(graph.adjacency[9, 9], 0)


if __name__ == '__main__':
    unittest.main()
