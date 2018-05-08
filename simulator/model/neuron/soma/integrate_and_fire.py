import math

from typing import Callable

from simulator.core import ActorRef
from simulator.model.neuron.events import ActionPotential, Spike
from simulator.model.neuron.soma.soma import Soma


class IntegrateAndFire(Soma):
    def __init__(self,
                 dendrites_generator: Callable[[ActorRef], ActorRef],
                 axon_generator: Callable[[ActorRef], ActorRef],
                 u_rest: float = 0.0,
                 tau=5.0):
        Soma.__init__(self, dendrites_generator, axon_generator)

        self.u = 0.0
        self.u_rest = u_rest
        self.threshold = 25.0
        self.tau = tau

    def apply(self, message):
        if isinstance(message, ActionPotential):
            current, timing = message

            self.u = self.u_rest + (self.u - self.u_rest) * math.exp((self.time - timing) / self.tau)
            self.u += current
            self.time = timing

            if self.u > self.threshold:
                self.last_spike = timing
                self.axon.send(Spike(timing=timing, sender_id=self.ref.id))
