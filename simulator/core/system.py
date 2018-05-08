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

        actor_ref = ActorRef(actor=actor, system=self, id=id)

        self.actors[id] = actor_ref
        if actor.__class__ not in self.actors_classes.keys():
            self.actors_classes[actor.__class__] = []
        self.actors_classes[actor.__class__].append(actor_ref)
        self.event_bus.subscribe(actor_ref)

        return actor_ref

    def kill(self, actor_ref, called_from_actor=False):
        self.actors.pop(actor_ref.id)
        self.actors_classes[actor_ref._actor.__class__].remove(actor_ref)
        self.event_bus.unsubscribe(actor_ref)

        if not called_from_actor:
            del actor_ref

    def broadcast(self, message, actor_class=None):
        if actor_class is None:
            for actor in self.actors.values():
                actor.send(message)
        else:
            for actor in self.actors_classes[actor_class]:
                actor.send(message)

    def run(self, **kwargs):
        self.event_bus.run(**kwargs)

    def get_by_id(self, id) -> ActorRef:
        return self.actors[id]


