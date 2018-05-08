from copy import copy

from simulator.core import Event


class ActorRef:
    def __init__(self, actor, system, id):
        self._actor = copy(actor)
        self._system = system
        self._id = id
        self._actor._ref = self

        actor.on_start()

    @property
    def id(self):
        return self._id

    @property
    def system(self):
        return self._system

    def send(self, message, timing=None):
        if timing is None:
            timing = self._system.event_bus.time
        self._system.event_bus.add_event(
            Event(data=message,  timing=timing, target_id=self._id)
        )

    def kill(self):
        self._actor.on_die()
        self._system.kill(self, called_from_actor=True)

    def __del__(self):
        self._actor.on_die()
        self._system.kill(self, called_from_actor=True)

    def ask(self, message):
        return self._actor.ask(message)
