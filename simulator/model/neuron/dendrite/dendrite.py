from abc import ABC, abstractmethod
from typing import List, Any, Dict

from simulator.core import ActorRef
from simulator.core.actor import Actor
from simulator.model.neuron.events import NewSynapse, HasFreeSpine


class DendriteBranch(Actor, ABC):
    def __init__(self, quotas: Dict[int, int], **kwargs):
        super(DendriteBranch, self).__init__(**kwargs)
        self.branches: List[ActorRef] = []
        self.synapses: List[ActorRef] = []
        self.quotas = quotas

    @abstractmethod
    def apply(self, message):
        pass

    def receive(self, message):
        if isinstance(message, NewSynapse):
            type = message.synapse.ask('type')
            self.quotas[type] = max(self.quotas[type] - 1, 0)
            self.synapses.append(message.synapse)

    def ask(self, message: Any) -> Any:
        if isinstance(message, HasFreeSpine):
            type = message.type
            return type in self.quotas.keys() and self.quotas[type] > 0
