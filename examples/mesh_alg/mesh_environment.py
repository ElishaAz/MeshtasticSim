from examples.mesh_alg.mesh_messages import MeshSendingMessage, MeshReceivingMessage
from examples.mesh_alg.utils import rssi_at_distance, distance_between
from mesh_logger import MeshLogger
from mesh_node import MeshNode
from meshtastic_sim import Environment, Simulator

N = MeshNode
L = MeshLogger
S = MeshSendingMessage
R = MeshReceivingMessage


class MeshEnvironment(Environment[N, S, R]):
    def __init__(self, send_steps: int = 5):
        self.send_steps = send_steps
        self.sending_messages: dict[int, set[MeshNode]] = dict()
        self.step = 0

    def start(self, simulator: Simulator["MeshEnvironment", N, L, S, R]):
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

    def receiving(self, step: int, receiver: N,
                  sent_now_messages: dict[N, S], sent_messages: dict[N, tuple[S, int]]) -> N | None:
        for sender, message in sent_now_messages.items():
            distance = distance_between(receiver, sender)
            rssi = rssi_at_distance(message.tx_power, distance)
            if rssi >= receiver.sensitivity:
                return sender
        return None

    def interfering(self, step: int, receiver: N, receiving_from: N, sent_messages: dict[N, tuple[S, int]]) -> bool:
        pass  # TODO: Implement interference logic

    def finished_sending(self, step: int, sender: N, message: S, sent_step: int) -> bool:
        return sent_step + self.send_steps <= step

    def receives(self, step: int, receiver: N, sender: N, message: S, sent_step: int) -> R | None:
        distance = distance_between(receiver, sender)
        rssi = rssi_at_distance(message.tx_power, distance)
        if rssi < receiver.sensitivity:
            return None

        return MeshReceivingMessage(rssi, message.message)
