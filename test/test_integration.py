import unittest

from pandas import DataFrame

from keybind_generator.data.SpreadsheetReader import SpreadsheetReader
from keybind_generator.solver.PepegaSolver import PepegaSolver
from keybind_generator.util.Graph import Graph
from keybind_generator.util.KeyBinding import KeyBinding
from keybind_generator.util.Keyboard import Keyboard
from test import base_dir


class TestIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.keyboard = Keyboard()
        cls.keyboard.add_key_row(Keyboard.KeyRow(0, 2, ["F1", "F2", "F3", "F4", "F5", "F6"]))
        cls.keyboard.add_key_row(Keyboard.KeyRow(1.5, 1, ["1", "2", "3", "4", "5", "6", "7"]))
        cls.keyboard.add_key_row(Keyboard.KeyRow(1.5, 1, ["1", "2", "3", "4", "5", "6", "7"]),
                                 modifier="Shift", modifier_penalty=4)

        cls.keyboard.add_key_row(Keyboard.KeyRow(2.5, 1.5, ["Q", "W", "E", "R", "T", "Y"]))
        cls.keyboard.add_key_row(Keyboard.KeyRow(2.5, 1.5, ["Q", "W", "E", "R", "T", "Y"]),
                                 modifier="Shift", modifier_penalty=4)
        cls.keyboard.add_key_row(Keyboard.KeyRow(2.5, 1.5, ["Q", "W", "E", "R", "T"]),
                                 modifier="Alt", modifier_penalty=8)

        cls.keyboard.add_key_row(Keyboard.KeyRow(3.5, 1.8, ["A", "S", "D", "F", "G", "H"]))
        cls.keyboard.add_key_row(Keyboard.KeyRow(3.5, 1.8, ["A", "S", "D", "F", "G"]),
                                 modifier="Shift", modifier_penalty=4)
        cls.keyboard.add_key_row(Keyboard.KeyRow(3.5, 1.8, ["A", "S", "D", "F", "G"]),
                                 modifier="Alt", modifier_penalty=8)

        cls.keyboard.add_key_row(Keyboard.KeyRow(4.5, 2, ["Z", "X", "C", "V", "B", "N"]))
        cls.keyboard.add_key_row(Keyboard.KeyRow(4.5, 2, ["Z", "X", "C", "V", "B"]),
                                 modifier="Shift", modifier_penalty=4)
        cls.keyboard.add_key_row(Keyboard.KeyRow(4.5, 2, ["Z", "X", "C", "V", "B"]),
                                 modifier="Alt", modifier_penalty=8)

        cls.keyboard.add_mouse_keys(["Mouse1", "Mouse2", "Mouse3", "Mouse4", "Mouse5", "Mouse6", "Mouse7", "Mouse8",
                                     "Mouse9", "Mouse10", "Mouse11", "Mouse12"], mouse_penalty=5)
        cls.keyboard.add_mouse_keys(["Mouse1", "Mouse2", "Mouse3", "Mouse4", "Mouse5", "Mouse6", "Mouse7", "Mouse8",
                                     "Mouse9", "Mouse10", "Mouse11", "Mouse12"],
                                    mouse_penalty=5, modifier="Shift", modifier_penalty=4)
        cls.keyboard.add_mouse_keys(["Mouse1", "Mouse2", "Mouse3", "Mouse4", "Mouse5", "Mouse6", "Mouse7", "Mouse8",
                                     "Mouse9", "Mouse10", "Mouse11", "Mouse12"],
                                    mouse_penalty=5, modifier="Alt", modifier_penalty=4)

    def test_random_solver_actual(self):
        spreadsheet_reader = SpreadsheetReader(str(base_dir) + "\\assets\\abilities.xlsx")
        abilities: DataFrame = spreadsheet_reader.read_abilities("Magic DW Abilities")
        combinations = spreadsheet_reader.read_combinations(abilities, "Magic Combinations")

        graph: Graph = self.keyboard.generate_graph()
        home_nodes = graph.get_node_indices(["A", "S", "D", "F"])

        print(home_nodes)

        random_solver = PepegaSolver(graph, abilities, combinations, home_nodes)

        random_solver.do_num_iter(1000)

        print(random_solver.best_binding)
        print(f"Best loss: %f" % random_solver.best_loss)

    def test_predefined_loss(self):
        # [print(entry) for entry in self.keyboard.entries]

        spreadsheet_reader = SpreadsheetReader(str(base_dir) + "\\assets\\abilities.xlsx")
        abilities: DataFrame = spreadsheet_reader.read_abilities("Magic DW Abilities")
        combinations = spreadsheet_reader.read_combinations(abilities, "Magic Combinations")
        graph: Graph = self.keyboard.generate_graph()
        home_nodes = graph.get_node_indices(["A", "S", "D", "F"])
        spreadsheet_bindings = spreadsheet_reader.read_binds("Magic Hand Binds")

        binding = KeyBinding(graph, abilities, combinations, home_nodes)
        binding.assign_from_data(spreadsheet_bindings)

        print(binding.eval_loss())
        print(binding)


if __name__ == '__main__':
    unittest.main()
