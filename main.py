import sys

from simulator.core import System, ActorRef, Event
from simulator.model import Logger
from simulator.model.neuron.events import Subscribe, ActionPotential
from simulator.model.neuron.soma import IntegrateAndFire
from simulator.model.neuron.synapse.plasticity import STDPPlasticity, DoubleSTDPPlasticity
from simulator.model.neuron.synapse.plasticity.InhibitorySTDP import InhibitorySTDPPlasticity
from simulator.model.neuron.synapse.plasticity.RewardSTDP import RewardSTDP
from simulator.network.ensemble import Ensemble, random_rule, all_to_all, default_dendrite_generator, axon_generator
from simulator.network.network import Network
from simulator.utils import flatten

from random import choice, random, randint, choices

import numpy as np
import matplotlib.pyplot as plt

sys.setrecursionlimit(35000)  # Required for saving very recursive data structures like our network


load = False


def main():
    print('Creating system...')

    net = Network()

    print('Creating neuronal group...')
    net.logger = net.system.spawn(Logger())

    output_logger = net.system.spawn(Logger())

    e_axon_gen = axon_generator(
        RewardSTDP(
            limit=4.0,
            w=1.5,
            trace_decay_speed=1.0,
            positive_decay_speed=0.25,
            negative_decay_speed=0.25
        ),
        delay=0.15
    )
    i_axon_gen = axon_generator(
        InhibitorySTDPPlasticity(
            limit=4.5,
            w=1.5,
            trace_decay_speed=1.0,
            negative_decay_speed=0.5,
            positive_decay_speed=0.5
        ),
        delay=0.25
    )

    group = Ensemble(
        size=9,
        network=net,
        neuron_proto=IntegrateAndFire(
            axon_generator=e_axon_gen,
            dendrites_generator=default_dendrite_generator
        )
    )

    hidden_group = Ensemble(
        size=15,
        network=net,
        neuron_proto=IntegrateAndFire(
            axon_generator=e_axon_gen,
            dendrites_generator=default_dendrite_generator
        )
    )

    out_group = Ensemble(
        size=2,
        network=net,
        neuron_proto=IntegrateAndFire(
            axon_generator=e_axon_gen,
            dendrites_generator=default_dendrite_generator
        )
    )

    i_group = Ensemble(
        size=10,
        network=net,
        neuron_proto=IntegrateAndFire(
            axon_generator=i_axon_gen,
            dendrites_generator=default_dendrite_generator
        )
    )

    del e_axon_gen

    for neuron_ref in group.neurons:
        neuron_ref.send(Subscribe(subscriber_ref=net.logger))

    for neuron_ref in hidden_group.neurons:
        neuron_ref.send(Subscribe(subscriber_ref=net.logger))

    out_group.neurons[0].send(Subscribe(subscriber_ref=output_logger))

    print('Creating synaptic connections...')

    group.connect(group, all_to_all)
    group.connect(hidden_group, all_to_all)
    hidden_group.connect(hidden_group, all_to_all)
    hidden_group.connect(out_group, all_to_all)
    out_group.connect(out_group, all_to_all)
    i_group.connect(group, all_to_all)
    group.connect(i_group, all_to_all)
    i_group.connect(out_group, all_to_all)

    net.run(stop_time=0.00001)

    print('Done.')
    print('Spawning actors...')

    print('Done.')
    print('Simulating...')

    xor = [
        ([0, 1], [1]),
        ([1, 0], [1]),
        ([1, 1], [0]),
        ([0, 0], [0])
    ]

    correct = 0
    incorrect = 0

    thr = 2

    while net.time < 2009.0:
        print(net.time)

        events = []

        xor_part = choice(xor)

        if xor_part[0][0] == 1:
            for i, neuron in enumerate(group.neurons[:3]):
                for j in range(4):
                    timing = net.time + (j / 2)
                    value = 15.0
                    target_id = neuron.id
                    events.append(
                        Event(
                            data=ActionPotential(timing=timing, value=value),
                            timing=timing,
                            target_id=target_id
                        )
                    )

        if xor_part[0][1] == 1:
            for i, neuron in enumerate(group.neurons[3:6]):
                for j in range(4):
                    timing = net.time + (j / 2)
                    value = 15.0
                    target_id = neuron.id
                    events.append(
                        Event(
                            data=ActionPotential(timing=timing, value=value),
                            timing=timing,
                            target_id=target_id
                        )
                    )

        for i, neuron in enumerate(group.neurons[6:9]):
            for j in range(4):
                timing = net.time + (j / 2)
                value = 15.0
                target_id = neuron.id
                events.append(
                    Event(
                        data=ActionPotential(timing=timing, value=value),
                        timing=timing,
                        target_id=target_id
                    )
                )

        net.add_events(events)
        net.run(stop_time=net.time + 1.0)

        spikes = output_logger.ask('get_and_delete_log')

        spikes = [] if out_group.neurons[0].id not in spikes.keys() else spikes[out_group.neurons[0].id]

        print(xor_part[0], xor_part[1], len(spikes))

        if (len(spikes) < thr and xor_part[1][0] == 1) or (len(spikes) > thr and xor_part[1][0] == 0):
            net.reinforce(-0.05 * abs(len(spikes) - xor_part[1][0] * thr) / thr)
            incorrect += 1
        else:
            correct += 1
            net.reinforce(0.05 * abs(len(spikes) - xor_part[1][0] * thr) / thr)

        net.run(stop_time=net.time + 1.0)

    print('Done.')

    print(correct, incorrect)

    spikes = net.logger.ask('get_log')
    spikes = flatten([value for key, value in spikes.items()])

    senders = list(set([sender for _, sender in spikes]))
    senders.sort()

    senders = {senders[i]: i for i in range(len(senders))}
    spikes = [(senders[sender], timing) for timing, sender in spikes]

    print('Total spikes: %d' % len(spikes))

    # spikes_matrix = np.zeros((36, 2010))
    #
    # for sender, timing in spikes:
    #     spikes_matrix[sender, int(timing)] = 1.0
    #
    # plt.matshow(spikes_matrix)
    # plt.savefig('example.png')

    Network.save(net, 'net.pickle')


if __name__ == '__main__':
    main()
