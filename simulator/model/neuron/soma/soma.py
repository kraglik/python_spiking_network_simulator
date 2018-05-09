from abc import ABC, abstractmethod
from typing import Any, Optional

from simulator.core.actor import Actor
from simulator.model.neuron.events import Spike, Connect, SubscriptionMessage, Subscribe, SpikeTrace


class Soma(Actor, ABC):
    def __init__(self, dendrites_generator, axon_generator, **kwargs):
        super(Soma, self).__init__(**kwargs)
        self._dendrites_generator = dendrites_generator
        self._axon_generator = axon_generator
        self.last_spike = -100.0
        self.time = 0.0
        self.dendrites = None
        self.axon = None
        self.subscribers = set()

    def subscribe(self, actor_ref):
        self.subscribers.add(actor_ref)

    def on_start(self):
        self.dendrites = self._dendrites_generator(self.ref)
        self.axon = self._axon_generator(self.ref)

        del self._dendrites_generator
        del self._axon_generator

    @abstractmethod
    def apply(self, message) -> Optional[Spike]:
        raise NotImplementedError

    def receive(self, message: Any) -> Any:
        if isinstance(message, Connect):
            self.axon.send(message)
        elif isinstance(message, Subscribe):
            subscriber_ref = message.subscriber_ref
            self.subscribe(subscriber_ref)
        spike = self.apply(message)
        if spike:
            self.broadcast(spike)
            self.axon.send(spike)
            self.dendrites.send(SpikeTrace(timing=spike.timing))

    def ask(self, message):
        if message == 'get_dendrite':
            return self.dendrites
        elif message == 'get_axon':
            return self.axon
        return None

    def on_die(self):
        self.dendrites.kill()
        self.axon.kill()

    def broadcast(self, message):
        for subscriber in self.subscribers:
            subscriber.send(SubscriptionMessage(data=message, sender_id=self.ref.id))
