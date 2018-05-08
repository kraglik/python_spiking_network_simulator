from copy import copy

from simulator.core.actor_ref import ActorRef
from simulator.core.event_bus import EventBus


class System:
    def __init__(self):
        self.event_bus = EventBus()
        self.actors_count = 0
        self.actors = dict()
        self.actors_classes = dict()

    def spawn(self, actor) -> ActorRef:
        self.actors_count += 1
        id = self.actors_count

        actor_ref = ActorRef(actor=copy(actor), system=self, id=id)

        self.actors[id] = actor_ref
        if actor.__class__ not in self.actors_classes.keys():
            self.actors_classes[actor.__class__] = []
        self.actors_classes[actor.__class__].append(actor_ref)
        self.event_bus.subscribe(actor)

        return actor_ref

    def broadcast(self, message, actor_class = None):
        if actor_class is None:
            for actor in self.actors.values():
                actor.send(message)
        else:
            for actor in self.actors_classes[actor_class]:
                actor.send(message)


