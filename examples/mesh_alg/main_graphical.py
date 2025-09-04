from examples.mesh_alg.mesh_environment import MeshEnvironment
from examples.mesh_alg.mesh_logger import MeshLogger
from examples.mesh_alg.mesh_messages import MeshMessage, HeaderFlags, MeshReceivingMessage, MeshSendingMessage
from examples.mesh_alg.mesh_node import MeshNode
from meshtastic_sim import Simulator, Node, Graphics

if __name__ == '__main__':
    logger = MeshLogger()
    environment = MeshEnvironment()

    sim = Simulator[MeshEnvironment, MeshNode, MeshLogger, MeshSendingMessage, MeshReceivingMessage]([], environment, logger)
    scale = 100
    tx_power = 10 # 10dm
    sensitivity = 1e-8 # -80 dbm

    i = 0


    def create_node(location: tuple[float, float]) -> Node:
        global i
        i += 1
        return MeshNode(i, str(i - 1), location, tx_power, sensitivity, environment)

    def on_start():
        sim.nodes[0].send_message(MeshMessage(2, 1, 0, HeaderFlags(10, True, False, 10), 0, 0, 0, "Hello World!"))


    graphics = Graphics(sim, create_node, scale, step_interval=0.1, on_start=on_start)
    graphics.main()
