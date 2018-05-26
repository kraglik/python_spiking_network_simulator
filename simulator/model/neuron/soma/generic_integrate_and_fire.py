import math

from typing import Callable

from simulator.core import ActorRef
from simulator.model.neuron.events import ActionPotential, Spike
from simulator.model.neuron.soma.soma import Soma


class GenericIntegrateAndFire(Soma):
    def __init__(self,
                 dendrites_generator: Callable[[ActorRef], ActorRef],
                 axon_generator: Callable[[ActorRef], ActorRef],
                 v_rest: float = -65.0,
                 v_reset: float = -70.0,
                 threshold: float = -50.0,
                 tau=15.0):
        Soma.__init__(self, dendrites_generator, axon_generator)

        self.v = 0.0
        self.v_rest = v_rest
        self.v_reset = v_reset
        self.threshold = threshold
        self.u = 0.0
        self.tau = tau

    def apply(self, message):
        if isinstance(message, ActionPotential):
            spike = None
            current, timing = message.value, message.timing

            self.v = self.v_rest + (self.v - self.v_rest) * math.exp(
                -(timing - self.time) / self.tau - (1.5) * (1.0 - math.exp())
            )
            self.v += current
            self.time = timing

            if self.v >= self.threshold:
                self.last_spike = timing
                self.v = self.v_reset
                spike = Spike(timing=timing, sender_id=self.ref.id)
            return spike