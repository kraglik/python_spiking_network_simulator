from copy import copy

from abc import ABC, abstractmethod
from typing import List, Optional, Callable

from simulator.core import ActorRef
from simulator.core.actor import Actor
from simulator.math.types import Point
from simulator.model.neuron.events import ActionPotential, Connect, NewSynapse, HasFreeSpine
from simulator.model.neuron.events import Spike
from simulator.model.neuron.synapse.synapse import Synapse


class AxonalBranch(Actor, ABC):
    def __init__(self,
                 parent: ActorRef = None,
                 start_point: Point = Point(0, 0, 0),
                 end_point: Point = Point(0, 0, 0),
                 synapse: Synapse = None,
                 type=0):
        self.id = id
        self.parent = parent
        self.synapses = []
        self.branches: List[ActorRef] = []
        self.connect_radius = 0.15
        self.type = type

        self.synapse = synapse

        self.start = start_point
        self.end = end_point

    @abstractmethod
    def map_spike(self, spike) -> Optional[Spike]:
        return spike

    def branch(self, points: List[Point], args, kwargs) -> List[ActorRef]:
        branches = []

        for point in points:
            branch = self.__class__(
                parent=self.ref,
                start_point=self.end,
                end_point=point,
                synapse=self.synapse,
                *args, **kwargs
            )
            branches.append(self.spawn(branch))

        return branches

    def transfer(self, spike: Spike):
        spike = self.map_spike(spike)

        for branch in self.branches:
            branch.send(spike)

    def transfer_backward(self, action_potential: ActionPotential):
        pass

    @abstractmethod
    def apply(self, message):
        pass

    def receive(self, message):
        if isinstance(message, Connect):
            soma_ref = self.system.get_by_id(message.target_id)
            dendrite_ref = soma_ref.ask('get_dendrite')
            can_connect = dendrite_ref.ask(HasFreeSpine(type=self.type))

            if can_connect:
                synapse_proto = copy(self.synapse)

                synapse_proto.input  = self.ref
                synapse_proto.output = dendrite_ref
                synapse_proto.type   = self.type

                synapse_ref = self.spawn(synapse_proto)

                dendrite_ref.send(NewSynapse(synapse_ref))