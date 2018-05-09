from typing import Any

from simulator.core import Actor
from simulator.model.neuron.axon import DelayedAxonalBranch


class Axon(Actor):

    def __init__(self, axonal_branch_proto=DelayedAxonalBranch):
        pass

    def receive(self, message: Any) -> Any:
        pass
