import random

from examples.mesh_alg.mesh_environment import MeshEnvironment
from examples.mesh_alg.mesh_logger import MeshLogger
from examples.mesh_alg.mesh_messages import MeshMessage, HeaderFlags
from examples.mesh_alg.mesh_node import MeshNode
from examples.mesh_alg.utils import random_packet_id
from meshtastic_sim import Simulator

if __name__ == '__main__':
    logger = MeshLogger()
    environment = MeshEnvironment()

    size = 500
    scale = 200
    count = 20
    tx_power = 10  # 10dm
    sensitivity = 1e-8  # -80 dbm

    nodes: list[MeshNode] = []

    for c in range(count):
        x = random.random() * size * scale
        y = random.random() * size * scale
        node = MeshNode(c + 1, str(c + 1), (x, y), tx_power, sensitivity, environment)
        nodes.append(node)

    message = MeshMessage(len(nodes), 1, random_packet_id(),
                          HeaderFlags(10, True, False, 10), 0, 0, 0, "Hello World!")
    nodes[0].send_message(message)

    sim = Simulator(nodes, environment, logger)
    sim.main(100)
