from abc import abstractmethod, ABC
from typing import Any

from simulator.core import Actor, ActorRef
from simulator.model.neuron.events import Spike, ActionPotential
from simulator.model.neuron.synapse.plasticity.plasticity_model import PlasticityModel
from simulator.model.neuron.synapse.plasticity.static import StaticPlasticityModel


class Synapse(Actor, ABC):
    def __init__(self,
                 input: ActorRef = None,
                 output: ActorRef = None,
                 plasticity_model: PlasticityModel = StaticPlasticityModel(),
                 type: int = 0):
        self.input = input
        self.output = output
        self.type = type
        self.plasticity_model = plasticity_model

    def receive(self, message):
        if isinstance(message, Spike):
            force = self.plasticity_model.apply_spike(message)
            self.output.send(ActionPotential(value=force, timing=message.timing))
        elif isinstance(message, ActionPotential):
            self.plasticity_model.apply_action_potential(message)

