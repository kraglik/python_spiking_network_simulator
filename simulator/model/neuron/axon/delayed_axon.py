from typing import Any, List

from simulator.math.types import Point
from simulator.model.neuron.events import Spike
from .axonal_branch import AxonalBranch
from random import random


class DelayedAxonalBranch(AxonalBranch):
    def __init__(self, parent, delay=random() * 5.0, **kwargs):
        super(DelayedAxonalBranch, self).__init__(parent, **kwargs)
        self.delay = delay

    def branch(self, points: List[Point], args, kwargs):
        super(self).branch(points, args, kwargs)

    def map_spike(self, spike: Spike):
        timing = spike.timing
        return Spike(timing=timing + self.delay, sender_id=spike.sender_id)

    def apply(self, message: Any) -> Any:
        pass


