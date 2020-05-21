import unittest
import xlrd
import numpy
from pandas import DataFrame, Series, Index

from keybind_generator.data.SpreadsheetReader import SpreadsheetReader
from test import base_dir


class TestSpreadsheetReader(unittest.TestCase):
    def test_read_abilities(self):
        spreadsheet_reader = SpreadsheetReader(str(base_dir) + "\\assets\\abilities.xlsx")
        abilities: DataFrame = spreadsheet_reader.read_abilities("Magic DW Abilities")
        self.assertTrue(numpy.array_equal(abilities.shape, [76, 4]))

    def test_read_combinations(self):
        spreadsheet_reader = SpreadsheetReader(str(base_dir) + "\\assets\\abilities.xlsx")
        abilities: DataFrame = spreadsheet_reader.read_abilities("Magic DW Abilities")

        combinations = spreadsheet_reader.read_combinations(abilities, "Magic Combinations")
        print(combinations)

        self.assertTrue(numpy.array_equal(combinations["indices"][0],
                                          [abilities["name"][abilities["name"] == "Wand Switch"].index[0],
                                           abilities["name"][abilities["name"] == "Shield Switch"].index[0],
                                           abilities["name"][abilities["name"] == "Resonance"].index[0]]))

        self.assertTrue(numpy.array_equal(combinations["indices"][1],
                                          [abilities["name"][abilities["name"] == "Target Cycle (Forwards)"].index[0],
                                           abilities["name"][abilities["name"] == "Spellbook Swap: Normal"].index[0],
                                           abilities["name"][abilities["name"] == "Vulnerability"].index[0]]))

        self.assertTrue(numpy.array_equal(combinations.shape, [24, 5]))

    def test_parse_combinations(self):
        ability_names = Series(["Ability 1", "Ability 2", "Ability 3"])
        ability_index = Index(ability_names)

        print(ability_index.get_loc("Ability 1"))

        print(ability_index)

        index = SpreadsheetReader.parse_combination_string(ability_index, "Ability 2 > Ability 1")
        self.assertTrue(numpy.array_equal(index, [1, 0]))
        pass


if __name__ == '__main__':
    unittest.main()
