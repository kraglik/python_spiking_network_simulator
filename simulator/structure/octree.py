from simulator.core import Actor, EventBus
from simulator.core.proxy import Proxy
from simulator.math.types import Point


class OctreeNode(Actor):

    def __init__(self, center: Point, side_len: float):

        self.center = center
        self.side_len = side_len

    def receive(self, event):
        return None

    def split(self):
        pass
