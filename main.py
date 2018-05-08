from simulator.core import System, ActorRef, Event
from simulator.model.neuron.events import Connect, ActionPotential, Subscribe
from simulator.model.neuron.soma import IntegrateAndFire
from simulator.model.neuron.dendrite import LinearDendriteBranch
from simulator.model.neuron.axon import DelayedAxonalBranch
from simulator.model.neuron.synapse import Synapse
from simulator.model import Logger
from simulator.utils import flatten

from random import choice, choices, random, randint

import numpy as np
import matplotlib.pyplot as plt


def main():
    system = System()

    print('Creating system...')

    logger_ref = system.spawn(Logger())

    def axon_generator(neuron_ref: ActorRef) -> ActorRef:
        return system.spawn(DelayedAxonalBranch(neuron_ref, synapse=Synapse()))

    def dendrite_generator(neuron_ref: ActorRef) -> ActorRef:
        return system.spawn(LinearDendriteBranch(parent=neuron_ref, quotas={0: 1000, 1: 2000}))

    neuron_proto = IntegrateAndFire(axon_generator, dendrite_generator)

    print('Done.')
    print('Spawning actors...')

    xs = [system.spawn(neuron_proto) for i in range(400)]
    ys = [system.spawn(neuron_proto) for i in range(400)]

    for neuron_ref in xs:
        neuron_ref.send(Subscribe(subscriber_ref=logger_ref))

    for neuron_ref in xs:
        for postsynaptic_ref in choices(ys, k=15):
            neuron_ref.send(Connect(target_id=postsynaptic_ref.id))

    for neuron_ref in ys:
        for postsynaptic_ref in choices(xs, k=15):
            neuron_ref.send(Connect(target_id=postsynaptic_ref.id))

    print('Done.')
    print('Simulating...')

    while system.time < 1000.0:
        events = []
        for i in range(randint(25, 125)):
            timing = system.time + random()
            value = 3.0 + random() * 8.0
            target_id = choice(xs).id
            events.append(
                Event(
                    data=ActionPotential(timing=timing, value=value),
                    timing=timing,
                    target_id=target_id
                )
            )
        system.event_bus.add_events(events)
        system.run(stop_time=system.time + 1)

    print('Done.')

    spikes = logger_ref.ask('get_log')
    spikes = flatten([value for key, value in spikes.items()])

    senders = list(set([sender for _, sender in spikes]))
    senders.sort()

    senders = {senders[i]: i for i in range(len(senders))}
    spikes = [(senders[sender], timing) for timing, sender in spikes]

    print('Generated spikes:')
    for sender, timing in spikes:
        print('    %d => spiked at %.2f milliseconds' % (sender, timing))

    print('Total spikes: %d' % len(spikes))

    spikes_matrix = np.zeros((400, 1001))

    for sender, timing in spikes:
        spikes_matrix[sender, int(timing)] = 1.0

    plt.matshow(spikes_matrix)
    plt.show()


if __name__ == '__main__':
    main()
