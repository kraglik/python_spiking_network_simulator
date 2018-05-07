from abc import ABC, abstractmethod
from typing import List, Optional

from simulator.core.actor import Actor
from simulator.model.neuron.events import Spike, ActionPotential
from simulator.utils import flatten


class AxonalBranch(Actor, ABC):
    def __init__(self, parent, id: int, **kwargs):
        super(AxonalBranch, self).__init__(**kwargs)
        self.id = id
        self.parent = parent
        self.synapses = []
        self.branches: List[AxonalBranch] = []

    @abstractmethod
    def map_spike(self, spike) -> Optional[Spike]:
        return spike

    def transfer(self, spike: Spike):
        spike = self.map_spike(spike)

        if spike is not None:
            events = flatten([branch.transfer(spike) for branch in self.branches])
            events += flatten([synapse.accept(spike) for synapse in self.synapses])
            return [x for x in events if x is not None]

        return []

    @abstractmethod
    def transfer_backward(self, action_potential: ActionPotential):
        pass
