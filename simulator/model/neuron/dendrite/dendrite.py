from abc import ABC, abstractmethod
from typing import List, Any, Dict

from simulator.core import ActorRef
from simulator.core.actor import Actor
from simulator.model.neuron.events import NewSynapse, HasFreeSpine, SpikeTrace


class DendriteBranch(Actor, ABC):
    def __init__(self, parent: ActorRef, quotas: Dict[int, int], **kwargs):
        super(DendriteBranch, self).__init__(**kwargs)
        self.branches: List[ActorRef] = []
        self.synapses: List[ActorRef] = []
        self.quotas = quotas
        self.parent = parent

    @abstractmethod
    def apply(self, message):
        pass

    def receive(self, message):
        if isinstance(message, NewSynapse):
            type = message.synapse_ref.ask('type')
            self.quotas[type] = max(self.quotas[type] - 1, 0)
            self.synapses.append(message.synapse_ref)
        if isinstance(message, SpikeTrace):
            for synapse in self.synapses:
                synapse.send(message)
            for branch in self.branches:
                branch.send(message)
        self.apply(message)

    def ask(self, message: Any) -> Any:
        if isinstance(message, HasFreeSpine):
            type = message.type
            return type in self.quotas.keys() and self.quotas[type] > 0
