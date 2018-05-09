from simulator.core import EventBus


class Proxy:
    def __init__(self, id, system, event_bus=None):
        self.event_bus = event_bus if event_bus is not None else EventBus()
        self._id = id
        self._system = system

    @property
    def subscribers(self):
        return self.event_bus.subscribers

    @property
    def id(self):
        return self._id

    @property
    def system(self):
        return self._system

    def send(self, event):
        self.event_bus.add_event(event)

    def run(self):
        self.event_bus.run()
