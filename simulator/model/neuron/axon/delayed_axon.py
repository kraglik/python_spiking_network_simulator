from simulator.model.neuron.events import Spike
from .axonal_branch import AxonalBranch


class DelayedAxonalBranch(AxonalBranch):
    def __init__(self, parent, delay=0.5):
        super(DelayedAxonalBranch, self).__init__(parent)
        self.delay = delay

    def map_spike(self, spike: Spike):
        timing = spike
        return Spike(timing=timing + self.delay)


