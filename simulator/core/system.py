from simulator.core.event_bus import EventBus


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
