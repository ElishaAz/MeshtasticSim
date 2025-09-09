from examples.mesh_alg.mesh_environment import MeshEnvironment
from examples.mesh_alg.mesh_logger import MeshLogger
from examples.mesh_alg.mesh_messages import MeshMessage, HeaderFlags, MeshReceivingMessage, MeshSendingMessage, Ack, Nak
from examples.mesh_alg.mesh_node import MeshNode
from examples.mesh_alg.utils import random_packet_id
from meshtastic_sim import Simulator, Node, Graphics

if __name__ == '__main__':
    logger = MeshLogger()
    environment = MeshEnvironment()

    sim = Simulator[MeshEnvironment, MeshNode, MeshLogger, MeshSendingMessage, MeshReceivingMessage]([], environment,
                                                                                                     logger)
    scale = 200
    tx_power = 10  # 10dm
    sensitivity = 1e-8  # -80 dbm

    i = 0


    def create_node(location: tuple[float, float]) -> Node:
        global i
        i += 1
        return MeshNode(i, str(i - 1), location, tx_power, sensitivity, environment)


    def on_start():
        sim.nodes[0].send_message(
            MeshMessage(len(sim.nodes), 1, random_packet_id(),
                        HeaderFlags(10, True, False, 10), 0, 0, 0, "Hello World!"))


    def color_for_message(message: MeshSendingMessage):
        if isinstance(message.message.payload, Ack):
            return 0, 255, 0, 255
        elif isinstance(message.message.payload, Nak):
            return 255, 0, 0, 255
        else:
            return 0, 0, 255, 255


    graphics = Graphics(sim, create_node, scale, step_interval=0.1, on_start=on_start,
                        color_for_message=color_for_message)
    graphics.main()
