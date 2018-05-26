from abc import ABC
import math


class EventBus(ABC):
    def __init__(self, time=0.0):
        self.events = [[]]
        self.events_cache = []
        self.time = time
        self.actors_count = 0
        self.subscribers = {}
        self.proxy_actors = {}

    def _merge_events_with_cache(self):
        self.events.extend(self.events_cache)
        self.events.sort(key=lambda event: event.timing)
        self.events_cache = []

    def subscribe(self, actor_ref):
        self.subscribers[actor_ref.id] = actor_ref

    def unsubscribe(self, actor_ref):
        self.subscribers.pop(actor_ref.id)

    def add_events(self, events):
        time = self.time
        for event in events:
            dt = 4 * int(event.timing - time) + int((event.timing % 1) / 4)

            while len(self.events) < (dt + 1):
                self.events.append([])

            self.events[dt].append(event)

    def add_event(self, event):
        self.add_events([event])

    def run(self, initial_events=None, stop_time=None):

        self.events.extend([] if initial_events is None else initial_events)

        while len(self.events) > 0 and (stop_time is None or self.time < stop_time):

            events = self.events[0]
            events.sort(key=lambda e: e.timing)

            while len(events) > 0 and (stop_time is None or self.time < stop_time):
                event = events.pop(0)
                self.time = event.timing
                actor_ref = self.subscribers[event.target_id]

                if actor_ref in self.proxy_actors.keys():
                    self.proxy_actors[actor_ref].send(event)
                else:
                    actor_ref._actor.receive(event.data)

            self.events.pop(0)

            print('Simulation time is ', self.time, 'ms', end='\r')

        if stop_time is not None:
            self.time = stop_time
