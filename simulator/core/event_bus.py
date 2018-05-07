from abc import ABC, abstractmethod

from simulator.core.actor import Actor


class EventBus(Actor, ABC):
    def __init__(self, time=0.0, *args, **kwargs):
        super(EventBus, self).__init__(*args, **kwargs)
        self.events = []
        self.events_cache = []
        self.time = time
        self.actors_count = 0
        self.subscribers = {}

    def _merge_events_with_cache(self):
        self.events.extend(self.events_cache)
        self.events.sort(key=lambda event: event.timing)
        self.events_cache = []

    def subscribe(self, actor):
        self.subscribers[actor.actor_system_id] = actor

    def unsubscribe(self, actor):
        self.subscribers.pop(actor.actor_system_id)

    def add_events(self, events):
        self.events_cache.extend(events)
        self._merge_events_with_cache()

    def run(self, initial_events=None):

        self.events.extend([] if initial_events is None else initial_events)

        while len(self.events) > 0:

            event = self.events.pop(0)
            self.time = event.timing
            target_actor = self.subscribers[event.target_id]

            response = target_actor.receive(event.data)

            if response is not None:

                if not isinstance(response, list):
                    response = [response]

                self.add_events(response)

    @abstractmethod
    def receive(self, event):
        return None
