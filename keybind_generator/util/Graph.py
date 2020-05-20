from typing import List, Union, Iterable

import numpy


class Graph:

    def __init__(self, size: int, names: List[str]):
        """
        Constructs a graph object (weighted, undirected)
        :param size: Number of nodes in the graph
        :param names: Names of the nodes
        """
        self.adjacency = numpy.zeros((size, size)) # Weights between nodes
        self.names = names

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
            length = length + self.adjacency[nodes[index],nodes[index+1]]

        return length
