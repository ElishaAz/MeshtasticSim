from typing import Any

from mesh_messages import MeshSendingMessage, MeshReceivingMessage
from mesh_node import MeshNode
from meshtastic_sim import Logger


class MeshLogger(Logger):
    def pre_step(self, step: int) -> None:
        print(F"============ Step {step} ============")

    def post_step(self, step: int) -> Any:
        pass

    def node_added(self, step: int, node: MeshNode) -> None:
        print(F"Node '{node.name}' added at {node.location}")

    def node_removed(self, step: int, node: MeshNode):
        pass

    def message_sent(self, step: int, node: MeshNode, message: MeshSendingMessage):
        print(F"Node '{node.name}' sent message")

    def message_received(self, step: int, node: MeshNode, message: MeshReceivingMessage):
        print(F"Node '{node.name}' received message")
