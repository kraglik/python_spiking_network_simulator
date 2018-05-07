from collections import namedtuple

from enum import Enum


class AxonalDelayType(Enum):
    OVERRIDE = 0
    DEFAULT = 1
    COMPLEMENT = 2


Spike = namedtuple('Spike', ['sender_id'])
ActionPotential = namedtuple('ActionPotential', ['value'])
AxonalBranching = namedtuple('AxonalBranching', ['point', 'delay', 'delay_type'])
BranchingCycle = namedtuple('BranchingCycle', ['radius'])

