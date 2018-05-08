from simulator.core import ActorRef
from simulator.model.neuron.dendrite import DendriteBranch
from typing import Dict

from simulator.model.neuron.events import ActionPotential


class LinearDendriteBranch(DendriteBranch):
    def __init__(self, parent: ActorRef, quotas: Dict[int, int], **kwargs):
        super(LinearDendriteBranch, self).__init__(parent, quotas, **kwargs)

    def apply(self, message):
        if isinstance(message, ActionPotential):
            self.parent.send(message)