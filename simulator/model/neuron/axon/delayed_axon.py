from typing import Any, List

from simulator.math.types import Point
from simulator.model.neuron.events import Spike
from .axonal_branch import AxonalBranch
from random import random


class DelayedAxonalBranch(AxonalBranch):
    def __init__(self, parent, delay=random() * 2.0):
        super(DelayedAxonalBranch, self).__init__(parent)
        self.delay = delay

    def branch(self, points: List[Point], args, kwargs):
        super(self).branch(points, args, kwargs)

    def map_spike(self, spike: Spike):
        timing = spike
        return Spike(timing=timing + self.delay)

    def apply(self, message: Any) -> Any:
        pass


