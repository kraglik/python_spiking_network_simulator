from abc import ABC


class EventBus(ABC):
    def __init__(self, time=0.0):
        self.events = []
        self.events_cache = []
        self.time = time
        self.actors_count = 0
        self.subscribers = {}

    def _merge_events_with_cache(self):
        self.events.extend(self.events_cache)
        self.events.sort(key=lambda event: event.timing)
        self.events_cache = []

    def subscribe(self, actor_ref):
        self.subscribers[actor_ref.id] = actor_ref

    def unsubscribe(self, actor_ref):
        self.subscribers.pop(actor_ref.id)

    def add_events(self, events):
        self.events_cache.extend(events)
        self._merge_events_with_cache()

    def add_event(self, event):
        self.add_events([event])

    def run(self, initial_events=None, stop_time=None):

        self.events.extend([] if initial_events is None else initial_events)

        while len(self.events) > 0 and (stop_time is None or self.time < stop_time):

            event = self.events.pop(0)
            self.time = event.timing
            actor_ref = self.subscribers[event.target_id]

            response = actor_ref._actor.receive(event.data)

            if response is not None:

                if not isinstance(response, list):
                    response = [response]

                self.add_events(response)
