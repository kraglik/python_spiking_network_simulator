from simulator.core import Actor, EventBus
from simulator.math.types import Point


class OctreeNode(Actor):

    def __init__(self, center: Point, side_len: float, time=0.0, *args, **kwargs):
        super(OctreeNode, self).__init__(time, *args, **kwargs)
        self.center = center
        self.side_len = side_len
        self.linked_nodes = []
        self.linked_nodes_notifications = 0

    def receive(self, event):
        self.run()
        return None

    def split(self):
        pass
