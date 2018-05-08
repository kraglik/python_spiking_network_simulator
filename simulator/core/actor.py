from abc import ABC, abstractmethod

from simulator.core import Event


class Actor(ABC):
    @abstractmethod
    def receive(self, event: Event):
        return None
