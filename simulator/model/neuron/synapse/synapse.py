from abc import abstractmethod, ABC
from typing import Any

from simulator.core import Actor, ActorRef
from simulator.model.neuron.events import Spike, ActionPotential, SpikeTrace, Reward
from simulator.model.neuron.synapse.plasticity import DoubleSTDPPlasticity
from simulator.model.neuron.synapse.plasticity.DecayingSTDP import DecayingSTDPPlasticity
from simulator.model.neuron.synapse.plasticity.plasticity_model import PlasticityModel
from simulator.model.neuron.synapse.plasticity.STDP import STDPPlasticity

from random import random


class Synapse(Actor, ABC):
    def __init__(self,
                 input: ActorRef = None,
                 output: ActorRef = None,
                 plasticity_model: PlasticityModel = STDPPlasticity(),
                 type: int = 0):
        self.input = input
        self.output = output
        self.type = type
        self.plasticity_model = plasticity_model

    def receive(self, message):
        if isinstance(message, Spike):
            force = self.plasticity_model.apply_spike(message)
            self.output.send(ActionPotential(value=force, timing=message.timing))
        elif isinstance(message, SpikeTrace):
            self.plasticity_model.update_traces(message)
        elif isinstance(message, Reward):
            self.plasticity_model.update_reward(message)

    def ask(self, message: Any) -> Any:
        if message == 'type':
            return self.type

