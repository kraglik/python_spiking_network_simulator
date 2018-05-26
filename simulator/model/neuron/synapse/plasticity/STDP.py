import math

from random import random

from simulator.model.neuron.events import SpikeTrace, Spike
from simulator.model.neuron.synapse.plasticity.plasticity_model import PlasticityModel


def clip(x, lo, hi):
    return max(lo, min(x, hi))


class STDPPlasticity(PlasticityModel):
    def __init__(self,
                 w=random(),
                 p=0.5,
                 nu_pre=1e-3,
                 nu_post=1e-3,
                 trace_decay_speed=1.0,
                 limit=1.0):
        PlasticityModel.__init__(self)
        self.w = w
        self.max_w = limit
        self.p = p
        self.nu_pre = nu_pre
        self.nu_post = nu_post
        self.pre_trace = 0
        self.post_trace = 0
        self.trace_decay_speed = trace_decay_speed

    def apply_spike(self, spike: Spike) -> float:
        self.last_input = spike.timing
        self.pre_trace += 1.0
        dt = spike.timing - max(self.last_output, self.last_input)
        self.post_trace = self.post_trace * math.exp(-dt * self.trace_decay_speed)
        self._update_weight(dt)
        return self.w

    def update_traces(self, spike_trace: SpikeTrace):
        dt = spike_trace.timing - max(self.last_output, self.last_input)
        self.last_output = spike_trace.timing
        self.post_trace += 1.0
        self.pre_trace = self.pre_trace * math.exp(-(spike_trace.timing - self.last_input) * self.trace_decay_speed)
        self._update_weight(dt)

    def _update_weight(self, dt):
        self.w += self.nu_post * self.pre_trace - self.nu_pre * self.post_trace
        self.w = clip(self.w, 0, self.max_w)
