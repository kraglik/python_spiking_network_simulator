from collections import namedtuple

from enum import Enum


class AxonalDelayType(Enum):
    OVERRIDE = 0
    DEFAULT = 1
    COMPLEMENT = 2


Spike = namedtuple('Spike', ['timing', 'sender_id'])

ActionPotential = namedtuple('ActionPotential', ['value', 'timing'])

AxonalBranching = namedtuple('AxonalBranching', ['point', 'delay', 'delay_type'])

BranchingCycle = namedtuple('BranchingCycle', ['radius'])

Connect = namedtuple('Connect', ['target_id'])

NewSynapse = namedtuple('NewSynapse', ['synapse_ref'])

HasFreeSpine = namedtuple('HasFreeSpine', ['type'])

SubscriptionMessage = namedtuple('SubscriptionMessage', ['data', 'sender_id'])

Subscribe = namedtuple('Subscribe', ['subscriber_ref'])
