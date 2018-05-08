from abc import ABC, abstractmethod


class Actor(ABC):
    @abstractmethod
    def receive(self, message):
        return None
