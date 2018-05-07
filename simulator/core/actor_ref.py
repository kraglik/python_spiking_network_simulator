from .system import System
from .actor import Actor


class ActorRef:
    def __init__(self, actor: Actor, system: System):
        self.actor = actor
        self.system = system

    def send(self, data, timing):
        self.system.create_event(data=data, timing=timing, target_id=self.actor.actor_system_id)

