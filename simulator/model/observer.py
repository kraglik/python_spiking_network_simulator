from typing import Any

from simulator.core import Actor
from simulator.model.neuron.events import SubscriptionMessage


class Logger(Actor):
    def __init__(self):
        self.log = dict()

    def receive(self, message):
        if isinstance(message, SubscriptionMessage):
            data, sender_id = message

            if sender_id not in self.log.keys():
                self.log[sender_id] = []

            self.log[sender_id].append(data)

        elif message == 'reset_log':
            self.log = dict()

    def ask(self, message: Any) -> Any:
        if message == 'get_log':
            return self.log
