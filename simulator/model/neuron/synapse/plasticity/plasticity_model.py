from abc import ABC, abstractmethod

from simulator.model.neuron.events import ActionPotential, Spike


class PlasticityModel(ABC):
    def __init__(self):
        self.last_input  = -1000.0
        self.last_output = -2000.0

    @abstractmethod
    def apply_spike(self, spike: Spike) -> float:
        raise NotImplementedError

    @abstractmethod
    def apply_action_potential(self, action_potential: ActionPotential):
        raise NotImplementedError
