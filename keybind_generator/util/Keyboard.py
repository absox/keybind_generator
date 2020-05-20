from abc import ABC, abstractmethod
from typing import List

from keybind_generator.util.Graph import Graph

import numpy


class Keyboard:
    class Key(ABC):
        """
        Abstract base class for Key entries, on mouse or on keyboard.
        """
        modifier_penalty: float
        modifier: str
        key: str

        def __str__(self):
            """
            Converts to string representation
            :return: String representation of the key
            """
            if self.modifier is None:
                return self.key
            return f"%s+%s" % (self.modifier, self.key)

        @abstractmethod
        def distance_to(self, other):
            """
            Distance to another key
            :param other: Key object to compute distance from this key to
            :return: Distance to the key
            """
            pass

    """
    Generates adjacency graphs for keyboards
    """
    class KeyEntry(Key):
        """
        Key entry which resides on the keyboard.
        """
        def __init__(self, key: str, x: float, y: float, modifier: str = "", modifier_penalty: float = 0):
            """
            Initializes key entry
            :param key: Name of key
            :param x: X-coordinate of key
            :param y: Y-coordinate of key
            :param modifier: Name of modifier (e.g. Shift, Alt, Ctrl)
            :param modifier_penalty:
            """
            self.key = key
            self.x = x
            self.y = y
            self.modifier = modifier
            self.modifier_penalty = modifier_penalty

        def distance_to(self, other):
            if isinstance(other, Keyboard.KeyEntry):
                # Return euclidean distance to other key entry
                distance = numpy.sqrt(numpy.square(other.x-self.x)+numpy.square(other.y-self.y))
            else:
                # Distance between keyboard keys and mouse keys and vice versa is 0
                distance = 0

            if other.modifier != self.modifier:
                distance = distance + other.modifier_penalty + self.modifier_penalty

            return distance

    class MouseKeyEntry(Key):
        """
        Key entry which resides on the mouse.
        """
        def __init__(self, key: str, mouse_penalty: float, modifier: str = "", modifier_penalty: float = 0):
            """
            Initializes key entry on mouse
            :param key: Name of key
            :param modifier: Name of modifier (e.g. Shift, Alt, Ctrl)
            :param mouse_penalty: Penalty incurred for repeating mouse presses
            :param modifier_penalty: Penalty incurred for changing modifiers
            """
            self.key = key
            self.modifier = modifier
            self.mouse_penalty = mouse_penalty
            self.modifier_penalty = modifier_penalty

        def distance_to(self, other):
            if isinstance(other, Keyboard.MouseKeyEntry):
                if other.key != self.key:
                    distance = other.mouse_penalty + self.mouse_penalty
                else:
                    distance = 0
            else:
                distance = 0

            if other.modifier != self.modifier:
                distance = distance + other.modifier_penalty + self.modifier_penalty

            return distance

    class KeyRow:
        def __init__(self, vertical_offset: float, horizontal_offset: float, keys: List[str]):
            """
            :param vertical_offset: space between the top of the keyboard and the start of the row
            :param horizontal_offset: space between the left of the keyboard and the start of the row
            """
            self.vertical_offset = vertical_offset
            self.horizontal_offset = horizontal_offset
            self.keys: List[str] = keys

    def __init__(self):
        """
        Constructs a keyboard object.
        """
        self.entries: List[Keyboard.Key] = []

    def add_key_row(self, key_row: KeyRow, modifier: str = "", modifier_penalty: float = 0) -> None:
        """
        Add a row of keys to the keyboard.
        :param key_row: KeyRow object containing the coordinates of keys
        :param modifier: Modifier key
        :param modifier_penalty: Distance penalty incurred for changing modifier
        :return:
        """

        for index, value in enumerate(key_row.keys):
            self.entries.append(Keyboard.KeyEntry(key_row.keys[index], key_row.horizontal_offset+index,
                                                      key_row.vertical_offset, modifier, modifier_penalty))

    def add_mouse_keys(self, keys: List[str], mouse_penalty: float, modifier: str = "", modifier_penalty: float = 0)\
            -> None:
        """
        Mouse keys have 0 distance to other keys (except for penalty incurred)
        :param keys: List of key names
        :param modifier: Modifier key
        :param mouse_penalty: Penalty incurred for using other mouse keys in succession
        :param modifier_penalty: Penalty incurred for changing modifier
        :return:
        """

        for key in keys:
            self.entries.append(Keyboard.MouseKeyEntry(key, mouse_penalty, modifier, modifier_penalty))

    def generate_graph(self) -> Graph:
        """
        Generates graph object from the keys in this Keyboard object
        :return: Graph representation of keyboard
        """
        # Count the total number of nodes, compute the names of keys
        size = len(self.entries)
        names = [str(entry) for entry in self.entries]
        graph = Graph(size, names)
        # Compute keyboard coordinates, and compute distances
        for i in range(size):
            for j in range(i+1, size):
                distance = self.entries[i].distance_to(self.entries[j])
                graph.adjacency[i, j] = distance
                graph.adjacency[j, i] = distance
        return graph
