from simulator.core import Event


class ActorRef:
    def __init__(self, actor, system, id):
        self._actor = actor
        self._system = system
        self._id = id

    @property
    def id(self):
        return self._id

    def send(self, message, timing=None):
        if timing is None:
            timing = self._system.event_bus.time
        self._system.event_bus.add_event(
            Event(
                data=message,
                timing=timing,
                target_id=self._id
            )
        )
