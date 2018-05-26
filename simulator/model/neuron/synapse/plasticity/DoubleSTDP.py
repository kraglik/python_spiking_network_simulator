import math

from random import random

from simulator.model.neuron.events import SpikeTrace, Spike
from simulator.model.neuron.synapse.plasticity.plasticity_model import PlasticityModel


class DoubleSTDPPlasticity(PlasticityModel):
    def __init__(self,
                 p=0.5,
                 nu_pre=1e-4,
                 nu_post=1e-2,
                 trace_decay_speed=0.01,
                 stabile_change_speed=0.005,
                 dynamic_change_speed=0.0075,
                 limit=2.0):
        PlasticityModel.__init__(self)
        self.w = random()
        self.w_stabile = random()
        self.max_w = limit
        self.p = p
        self.nu_pre = nu_pre
        self.nu_post = nu_post
        self.pre_trace = 0
        self.post_trace = 0
        self.trace_decay_speed = trace_decay_speed
        self.stabile_change_speed = stabile_change_speed
        self.dynamic_change_speed = dynamic_change_speed
        self.time = 0.0

    def apply_spike(self, spike):
        dt = spike.timing - max(self.last_output, self.last_input)
        self.last_input = spike.timing
        self.pre_trace = 1.0
        self.post_trace = self.post_trace * math.exp(-(spike.timing - self.last_output) * self.trace_decay_speed)
        self._update_weight(dt)
        self.time = spike.timing
        return self.w

    def update_traces(self, spike_trace):
        dt = spike_trace.timing - max(self.last_output, self.last_input)
        self.last_output = spike_trace.timing
        self.post_trace = 1.0
        self.pre_trace = self.pre_trace * math.exp(-(spike_trace.timing - self.last_input) * self.trace_decay_speed)
        self.time = spike_trace.timing

    def _update_weight(self, dt):
        w = self.w + self.nu_post * self.pre_trace - self.nu_pre * self.post_trace
        w += (self.w_stabile - w) * math.exp(-abs(dt) * self.dynamic_change_speed)
        self.w_stabile = (self.w_stabile - w) * (1.0 - math.exp(-abs(dt) * self.stabile_change_speed))
        self.w = max(0.0, min(self.max_w, self.w))
