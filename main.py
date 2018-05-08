from collections import namedtuple

from simulator.core import Actor, System


NameMessage = namedtuple('NameMessage', ['name'])


class Greeter(Actor):
    def receive(self, message):
        if isinstance(message, NameMessage):
            name = message.name
            print('Hello, ', name)


def main():
    system = System()
    greeter = Greeter()

    g1 = system.spawn(greeter)
    g2 = system.spawn(greeter)
    g3 = system.spawn(greeter)

    g1.send(NameMessage(name='Greeter #1'), timing=0.1)
    g2.send(NameMessage(name='Greeter #2'), timing=0.2)
    g3.send(NameMessage(name='Greeter #3'), timing=0.19)

    system.run(stop_time=0.16)

    g1.send(NameMessage(name='Late Greeter #1'), timing=0.18)

    system.run()


if __name__ == '__main__':
    main()
