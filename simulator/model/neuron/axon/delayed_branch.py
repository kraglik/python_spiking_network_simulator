from typing import List
from random import random

from simulator.core import ActorRef
from simulator.math.types import Point
from simulator.model.neuron.events import Spike, PSP
from .branch import AxonalBranch


class DelayedAxonalBranch(AxonalBranch):
    def __init__(self,
                 parent, delay=random() * 1.5,
                 start_point=Point(0, 0, 0),
                 end_point=Point(0, 0, 0)):
        AxonalBranch.__init__(self, parent, start_point, end_point)
        self.delay = delay

    def apply(self, spike: Spike):
        spike = Spike(timing=spike.timing + self.delay, sender_id=spike.sender_id)
        if self.leaf:
            for synapse_ref in self.synapses:
                synapse_ref.send(spike)
        else:
            for branch in self.branches:
                branch.apply(spike)

    def branch(self, points: List[Point], delays=None, *args, **kwargs):
        if self.can_branch:
            if delays is None:
                delays = [random() * 1.5 for _ in points]
            branches = []

            for i, point in enumerate(points):
                branches.append(
                    DelayedAxonalBranch(
                        parent=self,
                        start_point=self.end_point,
                        end_point=point,
                        delay=delays[i]
                    )
                )

            self.branches.extend(branches)

            self.leaf = False
            self.can_branch = True

            return [(points[i], branch) for i, branch in enumerate(branches)]
        return None

    def add_synapse(self, synapse_ref: ActorRef):
        self.synapses.append(synapse_ref)
        self.can_branch = False

    def apply_backward(self, psp: PSP):
        pass
