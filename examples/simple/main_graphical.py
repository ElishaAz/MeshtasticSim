from examples.simple.simple_environment import SimpleEnvironment
from examples.simple.simple_logger import SimpleLogger
from examples.simple.simple_node import SimpleNode
from meshtastic_sim import Simulator, Node, Graphics

if __name__ == '__main__':
    logger = SimpleLogger()
    environment = SimpleEnvironment()

    sim = Simulator([], environment, logger)
    radius = 20
    scale = 0.1

    i = 0


    def create_node(location: tuple[float, float]) -> Node:
        global i
        i += 1
        return SimpleNode(str(i - 1), location, radius)


    graphics = Graphics(sim, create_node, scale, step_interval=0.1)
    graphics.main()
