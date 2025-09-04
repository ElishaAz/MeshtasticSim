import random

from examples.simple.simple_environment import SimpleEnvironment
from examples.simple.simple_logger import SimpleLogger
from examples.simple.simple_message import SimpleMessage
from examples.simple.simple_node import SimpleNode
from meshtastic_sim import Simulator

if __name__ == '__main__':
    logger = SimpleLogger()
    environment = SimpleEnvironment()

    size = 10
    count = 10
    radius = 5

    nodes: list[SimpleNode] = []

    for c in range(count):
        x = random.random() * size
        y = random.random() * size
        node = SimpleNode(str(c), (x, y), radius)
        nodes.append(node)

    message = SimpleMessage(nodes[0], nodes[len(nodes) - 1], nodes[0], 5, random.randint(0, 2 ** 32 - 1))
    nodes[0].send_message(message)

    sim = Simulator(nodes, environment, logger)
    sim.main(50)