from typing import List

import pandas
import os

from pandas import DataFrame, Index

from keybind_generator.util.Keyboard import Keyboard


class SpreadsheetReader:
    """
    Reads in ability spreadsheets

    """

    @staticmethod
    def parse_combination_string(ability_names: Index, combination: str) -> List[int]:
        """
        Parses combination string
        :param ability_names:
        :param combination:
        :return:
        """
        return [ability_names.get_loc(entry.strip()) for entry in combination.split(">")]

        pass

    def __init__(self, file: str):
        """
        Initializer
        :param file:
        """
        self.file = file

        if os.path.splitext(file) is ".csv":
            self.type = "csv"
        else:
            self.type = "excel"

    def read_abilities(self, sheet_name: str = "") -> DataFrame:
        """
        Returns a data frame of abilities with their priority
        :param sheet_name:
        :return:
        """
        if self.type is "excel":
            data = pandas.read_excel(self.file, sheet_name)
        else:
            data = pandas.read_csv(self.file)
        data.columns = ["name", "priority", "bar", "comment"]
        return data

    def read_combinations(self, abilities: DataFrame, sheet_name: str = ""):
        """
        Returns a data frame of combinations with their priority
        :param abilities: Data frame of abilities
        :param sheet_name:
        :return:
        """
        if self.type is "excel":
            data: DataFrame = pandas.read_excel(self.file, sheet_name)
        else:
            data: DataFrame = pandas.read_csv(self.file)
        data.columns = ["name", "priority", "ordered", "comment"]
        data.insert(4, "indices", data["name"].apply(
            lambda entry: self.parse_combination_string(Index(abilities["name"]), entry)))

        return data

    def read_binds(self, sheet_name: str = ""):
        """
        Reads binds from a spreadsheet, returns a DataFrame in proper format
        :param sheet_name: Name of sheet within an excel file
        :return:
        """
        if self.type is "excel":
            data: DataFrame = pandas.read_excel(self.file, sheet_name, dtype={"Ability Name": str, "Bind": str})
        else:
            data: DataFrame = pandas.read_csv(self.file)
        data.columns = ["ability", "bind"]
        return data

    def read_keyboard_layout(self, sheet_name: str = "") -> Keyboard:
        """
        Reads a keyboard layout from a spreadsheet
        :param sheet_name:
        :return:
        """
        pass
