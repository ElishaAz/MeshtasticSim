from examples.mesh_alg.mesh_messages import MeshSendingMessage, MeshReceivingMessage
from examples.mesh_alg.utils import rssi_at_distance, distance_between, SendingState
from mesh_logger import MeshLogger
from mesh_node import MeshNode
from meshtastic_sim import Environment, Simulator


class MeshEnvironment(Environment):
    def __init__(self, send_steps: int = 5):
        self.send_steps = send_steps
        self.sending_messages: dict[int, set[MeshNode]] = dict()
        self.step = 0

    def start(self, simulator: Simulator["MeshEnvironment", MeshNode, MeshLogger]):
        pass

    def pre_step(self, step: int):
        self.step = step

        if step - self.send_steps - 1 in self.sending_messages:
            del self.sending_messages[step - self.send_steps - 1]

        self.sending_messages[self.step] = set()

    @staticmethod
    def _in_range(node: MeshNode, of: MeshNode) -> bool:

        distance = distance_between(node, of)
        rssi = rssi_at_distance(of.tx_power, distance)

        return rssi > node.sensitivity

    def do_cad(self, node: MeshNode) -> bool:
        """
        :param node:
        :return: True if the channel is clear for the node to send a message.
        """

        for nodes in self.sending_messages.values():
            for of in nodes:
                if self._in_range(node, of):
                    return False

        return True

    def try_send(self, node: MeshNode) -> bool:
        if self.is_sending(node) != SendingState.NOT_SENDING or not self.do_cad(node):
            return False

        self.sending_messages[self.step].add(node)

        return True

    def is_sending(self, node: MeshNode) -> SendingState:

        if (self.step - self.send_steps in self.sending_messages and
                node in self.sending_messages[self.step - self.send_steps]):
            return SendingState.FINISHED

        for nodes in self.sending_messages.values():
            if node in nodes:
                return SendingState.SENDING

        return SendingState.NOT_SENDING

    def receives(self, step: int, sender: MeshNode, receiver: MeshNode,
                 message: MeshSendingMessage) -> MeshReceivingMessage | None:
        distance = distance_between(receiver, sender)
        rssi = rssi_at_distance(message.tx_power, distance)
        if rssi < receiver.sensitivity:
            return None

        return MeshReceivingMessage(rssi, message.message)
