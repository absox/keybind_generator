import unittest

from pandas import DataFrame

from keybind_generator.data.SpreadsheetReader import SpreadsheetReader
from keybind_generator.solver.PepegaSolver import PepegaSolver
from keybind_generator.util.Graph import Graph
from keybind_generator.util.Keyboard import Keyboard
from test import base_dir


class TestIntegration(unittest.TestCase):
    def test_random_solver_actual(self):
        spreadsheet_reader = SpreadsheetReader(str(base_dir.parent) + "\\assets\\abilities.xlsx")
        abilities: DataFrame = spreadsheet_reader.read_abilities("Magic DW Abilities")
        combinations = spreadsheet_reader.read_combinations(abilities, "Magic Combinations")

        keyboard = Keyboard()
        keyboard.add_key_row(Keyboard.KeyRow(0, 2, ["F1", "F2", "F3", "F4"]))
        keyboard.add_key_row(Keyboard.KeyRow(1.5, 1, ["1", "2", "3", "4", "5", "6", "7"]))
        keyboard.add_key_row(Keyboard.KeyRow(1.5, 1, ["1", "2", "3", "4", "5", "6", "7"]),
                             modifier="Shift", modifier_penalty=4)

        keyboard.add_key_row(Keyboard.KeyRow(2.5, 1.5, ["Q", "W", "E", "R", "T", "Y"]))
        keyboard.add_key_row(Keyboard.KeyRow(2.5, 1.5, ["Q", "W", "E", "R", "T", "Y"]),
                             modifier="Shift", modifier_penalty=3)
        keyboard.add_key_row(Keyboard.KeyRow(2.5, 1.5, ["Q", "W", "E", "R", "T"]),
                             modifier="Alt", modifier_penalty=6)

        keyboard.add_key_row(Keyboard.KeyRow(3.5, 1.8, ["A", "S", "D", "F", "G", "H"]))
        keyboard.add_key_row(Keyboard.KeyRow(3.5, 1.8, ["A", "S", "D", "F", "G"]),
                             modifier="Shift", modifier_penalty=2)
        keyboard.add_key_row(Keyboard.KeyRow(3.5, 1.8, ["A", "S", "D", "F", "G"]),
                             modifier="Alt", modifier_penalty=4)

        keyboard.add_key_row(Keyboard.KeyRow(4.5, 2, ["Z", "X", "C", "V", "B", "N"]))
        keyboard.add_key_row(Keyboard.KeyRow(4.5, 2, ["Z", "X", "C", "V", "B"]),
                             modifier="Shift", modifier_penalty=2)
        keyboard.add_key_row(Keyboard.KeyRow(4.5, 2, ["Z", "X", "C", "V", "B"]),
                             modifier="Alt", modifier_penalty=4)

        keyboard.add_mouse_keys(["Mouse1", "Mouse2", "Mouse3", "Mouse4", "Mouse5", "Mouse6", "Mouse7", "Mouse8",
                                 "Mouse9", "Mouse10", "Mouse11", "Mouse12"], mouse_penalty=5)
        keyboard.add_mouse_keys(["Mouse1", "Mouse2", "Mouse3", "Mouse4", "Mouse5", "Mouse6", "Mouse7", "Mouse8",
                                 "Mouse9", "Mouse10", "Mouse11", "Mouse12"],
                                mouse_penalty=5, modifier="Shift", modifier_penalty=4)
        keyboard.add_mouse_keys(["Mouse1", "Mouse2", "Mouse3", "Mouse4", "Mouse5", "Mouse6", "Mouse7", "Mouse8",
                                 "Mouse9", "Mouse10", "Mouse11", "Mouse12"],
                                mouse_penalty=5, modifier="Alt", modifier_penalty=4)

        graph: Graph = keyboard.generate_graph()
        home_nodes = graph.get_node_indices(["A", "S", "D", "F"])

        print(home_nodes)

        random_solver = PepegaSolver(graph, abilities, combinations, home_nodes)

        random_solver.do_num_iter(1000)

        print(random_solver.best_binding)
        print(f"Best loss: %f" % random_solver.best_loss)


if __name__ == '__main__':
    unittest.main()
