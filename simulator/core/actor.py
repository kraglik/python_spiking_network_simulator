from abc import ABC, abstractmethod
from typing import Any

from simulator.core.system import System
from simulator.core.actor_ref import ActorRef


class Actor(ABC):
    @abstractmethod
    def receive(self, message):
        return None

    def on_start(self):
        pass

    def on_die(self):
        pass

    @property
    def ref(self) -> ActorRef:
        return self._ref

    @property
    def system(self) -> System:
        return self.ref.system

    def ask(self, message: Any) -> Any:
        return None

    def spawn(self, actor: 'Actor') -> ActorRef:
        return self.ref.system.spawn(actor)
