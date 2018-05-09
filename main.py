import sys

from simulator.core import System, ActorRef, Event
from simulator.model import Logger
from simulator.model.neuron.events import Subscribe, ActionPotential
from simulator.network.ensemble import Ensemble, random_rule, all_to_all
from simulator.network.network import Network
from simulator.utils import flatten

from random import choice, choices, random, randint

import numpy as np
import matplotlib.pyplot as plt

sys.setrecursionlimit(25000)

def main():
    print('Creating system...')

    net = Network()

    logger_ref = net.system.spawn(Logger())

    group = Ensemble(size=100, network=net)

    group.connect(group, random_rule(0.35))

    print('Done.')
    print('Spawning actors...')

    for neuron_ref in group.neurons:
        neuron_ref.send(Subscribe(subscriber_ref=logger_ref))

    net.run()

    print('Done.')
    print('Simulating...')

    while net.time < 499.0:
        events = []
        for i in range(randint(25, 45)):
            timing = net.time + random()
            value = 3.0 + random() * 8.0
            target_id = choice(group.neurons).id
            events.append(
                Event(
                    data=ActionPotential(timing=timing, value=value),
                    timing=timing,
                    target_id=target_id
                )
            )

        net.add_events(events)
        net.run(stop_time=net.time + 1)

    print('Done.')

    spikes = logger_ref.ask('get_log')
    spikes = flatten([value for key, value in spikes.items()])

    senders = list(set([sender for _, sender in spikes]))
    senders.sort()

    senders = {senders[i]: i for i in range(len(senders))}
    spikes = [(senders[sender], timing) for timing, sender in spikes]

    print('Total spikes: %d' % len(spikes))

    spikes_matrix = np.zeros((100, 500))

    for sender, timing in spikes:
        spikes_matrix[sender, int(timing)] = 1.0

    plt.matshow(spikes_matrix)
    plt.show()

    Network.save(net, 'net.pickle')


if __name__ == '__main__':
    main()
