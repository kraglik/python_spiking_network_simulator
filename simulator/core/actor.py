from abc import ABC, abstractmethod


class Actor(ABC):
    def __init__(self, actor_system_id=None, actor_system=None, supervisor=None, event_bus='system'):
        self.actor_system_id = actor_system_id
        self.actor_system = actor_system
        self.actor_system_supervisor = supervisor
        self.event_buses = [actor_system if event_bus == 'system' else event_bus]

    @abstractmethod
    def receive(self, event):
        return None

    def spawn(self, actor_class, *args, **kwargs):
        self.actor_system.spawn(actor_class, parent=self, *args, **kwargs)

    def subscribe(self, event_bus):
        if event_bus not in self.event_buses:
            self.event_buses.append(event_bus)
            event_bus.add_actor(self)

    def unsubscribe(self, event_bus):
        if event_bus not in self.event_buses:
            self.event_buses.remove(event_bus)
            event_bus.remove_actor(self)
