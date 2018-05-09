from simulator.core import System
import pickle


class Network:
    def __init__(self, name='network'):
        self.system = System()
        self.ensembles = set()

    def add_ensemble(self, ensemble):
        self.ensembles.add(ensemble)

    @property
    def time(self):
        return self.system.time

    def add_events(self, events):
        self.system.event_bus.add_events(events)

    def run(self, **kwargs):
        self.system.run(**kwargs)

    @staticmethod
    def save(net, filename):
        with open(filename, 'wb') as f:
            pickle.dump(net, f)

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)
