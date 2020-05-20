from typing import List

import numpy
from pandas import DataFrame

from keybind_generator.util.Graph import Graph


class KeyBinding:
    """
    Key binding class, for computing loss for a particular binding, as well as representing the model
    """

    def __init__(self, graph: Graph, abilities: DataFrame, combinations: DataFrame, home_nodes: List[int],
                 assignments: List[int] = None,
                 node_preference: List[float] = None, node_groups: List[int] = None, group_penalty: float = 0):
        """
        Initializes Key binding object.
        :param graph: Graph object for keys
        :param abilities: List of ability names, in order of assignment
        :param home_nodes: Index of home nodes
        :param node_preference: If certain nodes are to be preferred over others
        :param node_groups: If nodes are grouped (e.g. by finger)
        :param group_penalty: Penalty for repeating groups
        """

        self.graph = graph
        self.abilities = abilities
        self.combinations = combinations
        self.home_nodes = home_nodes

        self.node_preference: List[float] = []
        if node_preference is not None:
            self.node_preference = node_preference

        self.node_groups: List[int] = []
        if node_groups is not None:
            self.node_groups = node_groups

        self.group_penalty = group_penalty

        self.assignments: List[int] = []
        if assignments is not None:
            self.assignments = assignments

    def unassigned(self) -> numpy.array:
        """
        Returns list of unassigned indices
        :return:
        """
        return numpy.setdiff1d(range(self.graph.size), self.assignments)

    def has_assigned(self, index: int) -> bool:
        """
        Determines whether or not the index in question has already been assigned
        :param index: Key index we wish to assign
        :return: True if already assigned, false if not
        """
        return index in self.assignments

    def fully_assigned(self) -> bool:
        """
        Determines whether or not this key binding has assigned all abilities to keys
        :return: True if all abilities have been assigned, false if not
        """
        return len(self.assignments) == self.graph.size

    def assign_next(self, index: int) -> bool:
        """
        Assigns the next ability
        :param index: Index of key to assign next ability
        :return: True if success, false if unable
        """
        if not self.has_assigned(index) and len(self.assignments) < self.graph.size:
            self.assignments.append(index)
            return True
        else:
            return False

    def eval_loss(self) -> float:
        """
        Computes loss function for current binding
        :return: If not fully assigned, NaN. Else, the value of the loss function
        """
        if self.fully_assigned():
            # TODO
            return 0
        else:
            return numpy.nan
