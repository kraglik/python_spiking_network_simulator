from abc import ABC, abstractmethod


class Actor(ABC):
    def __init__(self, actor_system_id=None, actor_system=None, supervisor=None):
        self.actor_system_id = actor_system_id
        self.actor_system = actor_system
        self.actor_system_supervisor = supervisor

    @abstractmethod
    def receive(self, event):
        return None

    def spawn(self, actor_class, *args, **kwargs):
        self.actor_system.spawn(actor_class, parent=self, *args, **kwargs)

    def send(self, data, timing):
        self.actor_system.event_bus.create_event(
            target_id=self.actor_system_id,
            timing=timing,
            data=data
        )