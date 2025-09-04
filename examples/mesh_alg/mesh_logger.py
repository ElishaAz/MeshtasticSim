from typing import Any

from mesh_messages import MeshSendingMessage, MeshReceivingMessage
from mesh_node import MeshNode
from meshtastic_sim import Logger

N = MeshNode
S = MeshSendingMessage
R = MeshReceivingMessage


class MeshLogger(Logger):
    def pre_step(self, step: int) -> None:
        print(F"============ Step {step} ============")

    def post_step(self, step: int) -> Any:
        pass

    def node_added(self, step: int, node: N) -> None:
        print(F"Node '{node.name}' added at {node.location}")

    def node_removed(self, step: int, node: N):
        print(F"Node '{node.name}' removed from {node.location}")

    def started_sending(self, step: int, node: N, message: S) -> None:
        print(F"Node '{node.name}' started sending message", message.message.packet_id, message.message.payload)

    def interference(self, step: int, receiver: N, sender: N, message: S, step_sent: int) -> None:
        print(F"Interference at Node '{receiver.name}' from Node '{sender.name}' while receiving message",
              message.message.packet_id, message.message.payload)

    def finished_sending(self, step: int, node: MeshNode, message: S, sent_step: int):
        print(F"Node '{node.name}' finished sending message", message.message.packet_id, message.message.payload)

    def message_received(self, step: int, node: N, message: R):
        print(F"Node '{node.name}' received message", message.message.packet_id, message.message.payload)
