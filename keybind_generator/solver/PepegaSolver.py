import datetime
from datetime import timedelta
from typing import List

import numpy
from pandas import DataFrame
import progressbar

from keybind_generator.util.Graph import Graph
from keybind_generator.util.KeyBinding import KeyBinding


class PepegaSolver:
    """
    Random solver: pick a random key and bind an ability to it
    """

    def __init__(self, graph: Graph, abilities: DataFrame, combinations: DataFrame, home_node_indices: List[int]):
        self.best_binding: [KeyBinding, None] = None
        self.best_loss: numpy.float = numpy.inf
        self.num_iter = 0

        self.graph = graph
        self.abilities = abilities
        self.combinations = combinations
        self.home_node_indices = home_node_indices

    def run_iter(self):
        current_binding = KeyBinding(self.graph, self.abilities, self.combinations, self.home_node_indices)

        while not current_binding.fully_assigned():
            current_unassigned = current_binding.get_unassigned()
            choice = numpy.random.randint(0, len(current_unassigned))
            current_binding.assign_next(current_unassigned[choice])
        loss = current_binding.eval_loss()
        if loss < self.best_loss:
            print(f"New best loss: %f" % loss)
            self.best_loss = loss
            self.best_binding = current_binding
        self.num_iter = self.num_iter + 1  # Increment total number of iterations run by one

    def do_num_iter(self, num_iterations: int):
        for i in progressbar.progressbar(range(num_iterations)):
            self.run_iter()

    def do_time(self, time: timedelta) -> int:
        """
        :param time: Duration to run iterations for
        :return: Number of iterations done
        """
        start_time = datetime.datetime.now()
        iterations_run = 0
        while datetime.datetime.now() < start_time + time:
            self.run_iter()
            iterations_run = iterations_run + 1
        return iterations_run
