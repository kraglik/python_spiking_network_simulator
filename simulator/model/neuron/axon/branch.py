from abc import ABC, abstractmethod
from typing import List

from simulator.math.types import Point
from simulator.model.neuron.events import Spike, PSP


class AxonalBranch:
    def __init__(self, root, start_point=Point(0, 0, 0), end_point=Point(0, 0, 0)):
        self.start_point = start_point
        self.end_point = end_point
        self.root = root
        self.branches = []
        self.synapses = []
        self.leaf = True
        self.can_branch = True

    @abstractmethod
    def apply(self, spike: Spike):
        raise NotImplementedError

    @abstractmethod
    def apply_backward(self, psp: PSP):
        raise NotImplementedError

    @abstractmethod
    def branch(self, points: List[Point], *args, **kwargs):
        raise NotImplementedError
