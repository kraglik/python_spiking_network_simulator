from simulator.core.events import Event


class System:
    def __init__(self):
        self.events = []
        self.events_cache = []
        self.time = 0.0
        self.actors_count = 0
        self.subscribers = {}

    def _merge_events_with_cache(self):
        self.events.extend(self.events_cache)
        self.events.sort(key=lambda event: event.timing)
        self.events_cache = []

    def add_events(self, events):
        self.events_cache.extend(events)
        self._merge_events_with_cache()

    def run(self, initial_events=None, stop_time=None):

        self.events.extend([] if initial_events is None else initial_events)

        while len(self.events) > 0 and (stop_time is None or self.time < stop_time):

            event = self.events.pop(0)
            self.time = event.timing
            target_actor = self.subscribers[event.target_id]

            response = target_actor.receive(event.data)

            if response is not None:

                if not isinstance(response, list):
                    response = [response]

                self.add_events(response)

    def spawn(self, actor_class, supervisor='system', *args, **kwargs):
        actor_system_id = self.actors_count + 1

        kwargs['system'] = self
        kwargs['actor_system_id'] = actor_system_id
        kwargs['parent'] = self if supervisor == 'system' else supervisor

        actor = actor_class(*args, **kwargs)
        self.subscribers[actor_system_id] = actor

    def unsubscribe(self, actor):
        self.subscribers.pop(actor.actor_system_id)

    def subscribe(self, actor):
        self.subscribers[actor.actor_system_id] = actor

    def create_event(self, data, timing, target_id):
        event = Event(data=data, timing=timing, target_id=target_id)
        self.events_cache.append(event)
        self._merge_events_with_cache()


