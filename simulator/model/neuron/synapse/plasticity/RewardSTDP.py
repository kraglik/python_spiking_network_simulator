import math

from random import random

from simulator.model.neuron.events import SpikeTrace, Spike
from simulator.model.neuron.synapse.plasticity.plasticity_model import PlasticityModel


def clip(x, lo, hi):
    return max(lo, min(x, hi))


class RewardSTDP(PlasticityModel):
    def __init__(self,
                 w=random(),
                 nu_pre=1e-3,
                 nu_post=1e-3,
                 trace_decay_speed=1.0,
                 positive_decay_speed = 0.5,
                 negative_decay_speed = 0.5,
                 limit=1.0):
        PlasticityModel.__init__(self)
        self.w = w
        self.max_w = limit
        self.nu_pre = nu_pre
        self.nu_post = nu_post
        self.pre_trace = 0
        self.post_trace = 0
        self.positive_trace = 0.0
        self.negative_trace = 0.0
        self.reward_last_time = 0.0
        self.negative_decay_speed = negative_decay_speed
        self.positive_decay_speed = positive_decay_speed
        self.trace_decay_speed = trace_decay_speed

    def apply_spike(self, spike: Spike) -> float:
        self.last_input = spike.timing
        self.pre_trace += 1.0
        dt = spike.timing - max(self.last_output, self.last_input)
        self.post_trace = self.post_trace * math.exp(-dt * self.trace_decay_speed)
        self._update_weight()
        return self.w

    def update_traces(self, spike_trace: SpikeTrace):
        self.last_output = spike_trace.timing
        self.post_trace += 1.0
        self.pre_trace = self.pre_trace * math.exp(-(spike_trace.timing - self.last_input) * self.trace_decay_speed)
        self._update_weight()

    def _update_reward_traces(self, timing):
        self.negative_trace = self.negative_trace * math.exp(
            -(timing - self.reward_last_time) / self.negative_decay_speed
        )
        self.positive_trace = self.positive_trace * math.exp(
            -(timing - self.reward_last_time) / self.positive_decay_speed
        )
        self.positive_trace = clip(self.positive_trace, 0, 2.5)
        self.negative_trace = clip(self.negative_trace, 0, 2.5)
        self.reward_last_time = timing

    def update_reward(self, reward_event):
        timing, reward = reward_event
        self._update_reward_traces(timing)

        if reward > 0:
            self.positive_trace += reward
        else:
            self.negative_trace -= reward

        dt = timing - max(self.last_output, self.last_input)
        self.pre_trace = self.pre_trace * math.exp(-dt * self.trace_decay_speed)
        self.post_trace = self.post_trace * math.exp(-dt * self.trace_decay_speed)
        self.last_input = timing
        self.last_output = timing
        self._update_weight()

    def _update_weight(self):
        self._update_reward_traces(max(self.last_output, self.last_input))
        self.w += self.nu_post * self.pre_trace * self.positive_trace - self.nu_pre * self.post_trace * self.negative_trace
        self.w = clip(self.w, 0, self.max_w)
