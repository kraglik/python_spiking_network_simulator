from abc import ABC, abstractmethod

from simulator.model.neuron.events import Spike, SpikeTrace


class PlasticityModel(ABC):
    def __init__(self):
        self.last_input  = 0.0
        self.last_output = 0.0

    @abstractmethod
    def apply_spike(self, spike: Spike) -> float:
        raise NotImplementedError

    @abstractmethod
    def update_traces(self, spike_trace: SpikeTrace):
        raise NotImplementedError

    def update_reward(self, reward):
        pass
