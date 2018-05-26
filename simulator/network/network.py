from simulator.core import System
import pickle

from simulator.model.neuron.events import Reward
from simulator.model.neuron.synapse import Synapse


class Network:
    def __init__(self, name='network'):
        self.system = System()
        self.ensembles = set()

    def add_ensemble(self, ensemble):
        self.ensembles.add(ensemble)

    @property
    def time(self):
        return self.system.time

    def set_time(self, new_time):
        self.system.event_bus.time = new_time

    def add_events(self, events):
        self.system.event_bus.add_events(events)

    def run(self, **kwargs):
        self.system.run(**kwargs)

    def reinforce(self, value):
        self.system.broadcast(Reward(self.time, value), Synapse)

    @staticmethod
    def save(net, filename):
        with open(filename, 'wb') as f:
            pickle.dump(net, f)

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
