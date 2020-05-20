from typing import List, Union, Iterable

import numpy
from pandas import Index


class Graph:

    def __init__(self, size: int, names: List[str]):
        """
        Constructs a graph object (weighted, undirected)
        :param size: Number of nodes in the graph
        :param names: Names of the nodes
        """
        self.adjacency = numpy.zeros((size, size))  # Weights between nodes
        self.size = size
        self.names = names
        self.name_index = Index(names)

    def minimum_distance(self, nodes_from: Union[int, List[int]], nodes_to: Union[int, List[int]]) -> float:
        """
        Gets the minimum distance
        :param nodes_from: Index of node or nodes from which to compute the distance
        :param nodes_to: Index of node or nodes to which to compute the distance
        :return: Minimum distance between nodes
        """
        if isinstance(nodes_from, Iterable):
            return numpy.min([numpy.min(self.adjacency[i, nodes_to]) for i in nodes_from])
        return numpy.min(self.adjacency[nodes_from, nodes_to])

    def path_length(self, nodes: List[int]) -> float:
        """
        :param nodes:
        :return: Length of path
        """
        if len(nodes) is 1:
            return 0
        length = 0
        for index in range(len(nodes)-1):
            length = length + self.adjacency[nodes[index], nodes[index+1]]

        return length

    def get_node_index(self, name: str) -> int:
        """
        Gets index of node
        :param name: Name of node
        :return: index of node
        """
        return self.name_index.get_loc(name)

    def get_node_indices(self, names: List[str]) -> List[int]:
        return [self.get_node_index(name) for name in names]
