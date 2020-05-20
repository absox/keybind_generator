from typing import List

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

