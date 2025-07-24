from examples.simple.simple_environment import SimpleEnvironment
from examples.simple.simple_logger import SimpleLogger
from examples.simple.simple_node import SimpleNode
from meshtastic_sim import Simulator, Node
from meshtastic_sim.graphics import Graphics

if __name__ == '__main__':
    logger = SimpleLogger()
    environment = SimpleEnvironment()

    # size = 10
    # count = 10
    # radius = 5
    #
    # nodes: list[SimpleNode] = []
    #
    # for c in range(count):
    #     x = random.random() * size
    #     y = random.random() * size
    #     node = SimpleNode(str(c), (x, y), radius)
    #     nodes.append(node)
    #
    # message = SimpleMessage(nodes[0], nodes[len(nodes) - 1], nodes[0], 5, random.randint(0, 2 ** 32 - 1))
    # nodes[0].send_message(message)
    #
    # sim = Simulator(nodes, environment, logger)
    # sim.main(10)

    sim = Simulator([], environment, logger)
    radius = 20
    scale = 0.1

    i = 0


    def create_node(location: tuple[float, float]) -> Node:
        global i
        i += 1
        return SimpleNode(str(i - 1), location, radius)


    graphics = Graphics(sim, create_node, scale)
    graphics.main()