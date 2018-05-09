from typing import Any

from simulator.core import Actor
from simulator.model.neuron.axon import DelayedAxonalBranch


class Axon(Actor):

    def __init__(self, branch_proto):
        self.branch_proto = branch_proto

    def receive(self, message: Any) -> Any:
        pass
