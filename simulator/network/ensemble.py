from simulator.core import ActorRef
from simulator.model.neuron.axon import DelayedAxonalBranch
from simulator.model.neuron.dendrite import LinearDendriteBranch
from simulator.model.neuron.events import Connect
from simulator.model.neuron.soma import IntegrateAndFire
from simulator.model.neuron.synapse import Synapse
from simulator.network.network import Network
from random import random as rand


def default_axon_generator(system, neuron_ref: ActorRef) -> ActorRef:
    return system.spawn(DelayedAxonalBranch(neuron_ref, synapse=Synapse()))


def default_dendrite_generator(system, neuron_ref: ActorRef) -> ActorRef:
    return system.spawn(LinearDendriteBranch(parent=neuron_ref, quotas={0: 100000}))


def all_to_all(presynaptic, postsynaptic):
    return True


def random_rule(p=0.5):
    def random_connection(presynaptic, postsynaptic):
        return rand() < p
    return random_connection


def one_to_one(presynaptic, postsynaptic):
    return presynaptic == postsynaptic


class Ensemble:
    def __init__(self,
                 size: int,
                 network: Network,
                 neuron_proto=IntegrateAndFire(
                     axon_generator=default_axon_generator,
                     dendrites_generator=default_dendrite_generator)
                 ):
        self.neuron_proto = neuron_proto
        self.size = size
        self.network = network
        self.neurons = [self.network.system.spawn(self.neuron_proto) for _ in range(self.size)]

        network.add_ensemble(self)

    def connect(self, other: 'Ensemble', connection_rule):
        for i, pre in enumerate(self.neurons):
            for j, post in enumerate(other.neurons):
                if connection_rule(i, j):
                    pre.send(Connect(target_id=post.id))

