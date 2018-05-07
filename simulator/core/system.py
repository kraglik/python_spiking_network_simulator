from simulator.core.event_bus import EventBus
from simulator.core.events import Event


class System:
    def __init__(self):
        self.event_bus = EventBus()
        self.actors_count = 0

    def spawn(self, actor_class, supervisor='system', *args, **kwargs):
        actor_system_id = self.actors_count + 1

        kwargs['system'] = self
        kwargs['actor_system_id'] = actor_system_id
        kwargs['supervisor'] = self if supervisor == 'system' else supervisor

        actor = actor_class(*args, **kwargs)
        self.event_bus.subscribe(actor)

    def unsubscribe(self, actor):
        self.event_bus.unsubscribe(actor)

    def subscribe(self, actor):
        self.event_bus.subscribe(actor)


