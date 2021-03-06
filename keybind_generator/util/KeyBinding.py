from typing import List

import numpy
from pandas import DataFrame, Index

from keybind_generator.util.Graph import Graph


class KeyBinding:
    """
    Key binding class, for computing loss for a particular binding, as well as representing the model
    """

    def __init__(self, graph: Graph, abilities: DataFrame, combinations: DataFrame, home_nodes: List[int],
                 assignments: List[int] = None, node_priority: List[float] = None,
                 individual_coefficient: float = 1, combination_coefficient: float = 1):
        """
        Initializes Key binding object.
        :param graph: Graph object for keys
        :param abilities: List of ability names, in order of assignment
        :param home_nodes: Index of home nodes
        :param node_priority: If certain nodes are to be preferred over others

        """

        self.graph = graph
        self.abilities = abilities
        self.ability_index = Index(abilities["name"])
        self.combinations = combinations
        self.home_nodes = home_nodes
        self.unassigned: numpy.array = numpy.array(range(self.graph.size))

        self.node_priority: List[float] = []
        if node_priority is not None:
            self.node_priority = node_priority

        self.assignments: List[int] = []
        if assignments is not None:
            self.assignments = list(assignments)

        self.individual_coefficient = individual_coefficient
        self.combination_coefficient = combination_coefficient

    def assign_from_data(self, data: DataFrame):
        """
        Assigns keys from a data frame containing binding data
        :param data:
        :return:
        """
        self.assignments = [0] * self.abilities.shape[0]

        def assignment_function(row):
            # print(f"Assigning %s : %s" % (row["ability"], str(row["bind"])))

            ability_index = self.ability_index.get_loc(row["ability"])
            # print(f"Ability index: %d" % ability_index)

            bind_index = self.graph.get_node_index(row["bind"])
            # print(f"Bind index: %d" % bind_index)

            self.assignments[ability_index] = bind_index

        data.apply(assignment_function, axis=1)

        # TODO
        pass

    def get_unassigned(self) -> numpy.array:
        """
        Returns list of unassigned indices
        :return:
        """
        return self.unassigned
        # return numpy.setdiff1d(range(self.graph.size), self.assignments)

    def get_assignment(self, ability_name: str) -> [int, None]:
        """
        Gets the node index to which an ability has been assigned
        :param ability_name: Name of ability to find index
        :return:
        """
        ability_position = self.ability_index.get_loc(ability_name)
        if ability_position > len(self.assignments):
            return None
        return self.assignments[ability_position]

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
        return len(self.assignments) == self.abilities.shape[0]

    def assign_next(self, index: int) -> bool:
        """
        Assigns the next ability
        :param index: Index of key to assign next ability
        :return: True if success, false if unable
        """
        if not self.has_assigned(index) and len(self.assignments) < self.graph.size:
            self.assignments.append(index)
            self.unassigned = numpy.delete(self.unassigned, numpy.where(self.unassigned == index))
            return True
        else:
            return False

    def eval_loss(self) -> float:
        """
        Computes loss function for current binding
        :return: If not fully assigned, NaN. Else, the value of the loss function
        """
        if self.fully_assigned():
            """
            Loss formula: Individual term + Combination term
            
            Individual term is given by minimum distance to home divided by ability priority, plus node priority,
            summed over all abilities,

            Combination term is given by path distance for combinations divided by priority
            """

            # Minimum distance of each ability to the home nodes, divided by priority
            minimum_distances = [self.graph.minimum_distance(node, self.home_nodes) for node in self.assignments]

            ability_priorities = self.abilities["priority"]

            individual_terms = numpy.divide(minimum_distances, ability_priorities)

            if self.node_priority:
                individual_terms = numpy.add(individual_terms, self.node_priority)

            combination_terms = 0

            if self.combinations.shape[0]:
                combination_terms = numpy.divide([
                    self.graph.path_length(entry) for entry in self.combinations["indices"]],
                    self.combinations["priority"])

            return self.individual_coefficient * numpy.sum(individual_terms) +\
                   self.combination_coefficient * numpy.sum(combination_terms)
        else:
            return numpy.nan

    def __str__(self):
        """
        String representation of key binding
        :return: String representation of key binding
        """
        if not self.assignments:
            return ""

        ability_names = self.abilities["name"][0:len(self.assignments)]
        key_strings = [self.graph.names[entry] for entry in self.assignments]
        binding_strings = [value + " : " + key_strings[index] for index, value in enumerate(ability_names)]
        return "\n".join(binding_strings)