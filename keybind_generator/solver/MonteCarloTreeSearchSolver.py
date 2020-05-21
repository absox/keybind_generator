from typing import List

import numpy
import progressbar

from pandas import DataFrame

from keybind_generator.util.Graph import Graph
from keybind_generator.util.KeyBinding import KeyBinding


class MonteCarloTreeSearchSolver:

    class Node:
        """
        A Node in the monte carlo tree
        """
        def __init__(self, num_children):
            self.visits: int = 0
            self.loss: float = 0
            self.children: List = [None] * num_children

        @staticmethod
        def compute_uct(parent, child):
            if parent.visits == 0 or child.visits == 0:
                return 0
            # We add an epsilon to the loss in case loss is ever 0
            return 1 / (child.loss + .01) + numpy.sqrt(numpy.log(parent.visits) / child.visits)

        def update_loss(self, new_loss):
            self.loss = (self.loss * self.visits + new_loss)/(self.visits + 1)
            self.visits = self.visits + 1

        def run_iteration(self, binding: KeyBinding) -> (float, KeyBinding):
            # Leaf node
            if binding.fully_assigned():
                loss = binding.eval_loss()
                self.update_loss(loss)
                return loss, binding

            # If at least one child hasn't been visited, visit that child
            unvisited_children = [idx for idx, value in enumerate(self.children) if value is None]
            if len(unvisited_children) > 0:
                index = numpy.random.randint(0, len(unvisited_children))
                binding.assign_next(binding.unassigned[unvisited_children[index]])
                # Make sure we call copy constructor on list of assignments and bindings
                self.children[unvisited_children[index]] =\
                    MonteCarloTreeSearchSolver.Node(len(binding.unassigned))
                loss, binding = self.children[unvisited_children[index]].run_iteration(binding)
                self.update_loss(loss)
                return loss, binding
            else:
                # Else, visit the child with the highest UCT value
                uct_values = [MonteCarloTreeSearchSolver.Node.compute_uct(self, child) for child in self.children]
                indices = numpy.where(uct_values == numpy.max(uct_values))[0]
                index = numpy.random.randint(0, len(indices))
                binding.assign_next(binding.unassigned[indices[index]])
                loss, binding = self.children[indices[index]].run_iteration(binding)
                self.update_loss(loss)
                return loss, binding

    def __init__(self, graph: Graph, abilities: DataFrame, combinations: DataFrame, home_node_indices: List[int]):
        self.graph = graph
        self.abilities = abilities
        self.combinations = combinations
        self.home_node_indices = home_node_indices

        self.best_binding = None
        self.best_loss = numpy.inf

        binding = KeyBinding(self.graph, self.abilities, self.combinations, self.home_node_indices)
        self.root = MonteCarloTreeSearchSolver.Node(len(binding.unassigned))

    def run_iter(self) -> (float, KeyBinding):
        binding = KeyBinding(self.graph, self.abilities, self.combinations, self.home_node_indices)
        loss, binding = self.root.run_iteration(binding)

        if loss < self.best_loss:
            self.best_loss = loss
            self.best_binding = binding
        return loss, binding

    def do_num_iter(self, num_iterations) -> (float, KeyBinding):
        for i in progressbar.progressbar(range(num_iterations)):
            self.run_iter()
        return self.best_loss, self.best_binding

