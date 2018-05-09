from typing import Any

from simulator.core import Actor
from simulator.model.neuron.axon.delayed_branch import DelayedAxonalBranch
from simulator.model.neuron.axon.branch import AxonalBranch
from simulator.model.neuron.events import Spike


class Axon(Actor):

    def __init__(self, branch_proto: AxonalBranch):
        self.branches = []
        self.root_branch = branch_proto
        self.root_branch.root = self
        self.root = self.system.spawn(branch_proto)

    def receive(self, message: Any) -> Any:
        if isinstance(message, Spike):
            self.root_branch.apply(spike=message)
