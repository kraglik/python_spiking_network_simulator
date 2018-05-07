from abc import ABC, abstractmethod

from simulator.core.actor import Actor


class DendriteBranch(Actor, ABC):
    def __init__(self, branches=None, **kwargs):
        super(DendriteBranch, self).__init__(**kwargs)
        self.branches = [] if branches is None else branches

    @abstractmethod
    def receive(self, event):
        return None
