from abc import ABC, abstractmethod

from simulator.core.actor import Actor
from simulator.model.neuron.events import Spike


class Soma(Actor, ABC):
    def __init__(self, dendrites_generator, axon_generator, **kwargs):
        super(Soma, self).__init__(**kwargs)
        self.dendrites = dendrites_generator(self)
        self.axon = axon_generator(self)

    @abstractmethod
    def receive(self, event: Spike):
        return None

