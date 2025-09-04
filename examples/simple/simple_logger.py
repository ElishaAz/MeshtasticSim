from typing import Any

from meshtastic_sim import Logger, Node
from meshtastic_sim.logger import S
from meshtastic_sim.message import ReceivingMessage
from simple_message import SimpleMessage
from simple_node import SimpleNode


class SimpleLogger(Logger):
    def pre_step(self, step: int) -> None:
        print(F"============ Step {step} ============")

    def post_step(self, step: int) -> Any:
        pass

    def node_added(self, step: int, node: SimpleNode) -> None:
        print(F"Node '{node.name}' added at {node.location}")

    def node_removed(self, step: int, node: SimpleNode):
        print(F"Node '{node.name}' removed at {node.location}")

    def started_sending(self, step: int, node: Node, message: S) -> None:
        print(F"Started sending at {node.location}: {message}")

    def interference(self, step: int, receiver: Node, sender: Node, message: S, step_sent: int) -> None:
        print(F"Interference at {receiver.location}: {message}")

    def finished_sending(self, step: int, node: Node, message: S, sent_step: int) -> None:
        print(F"Finished sending at {node.location}, since step {sent_step}: {message}")

    def message_received(self, step: int, node: SimpleNode, message: ReceivingMessage[SimpleMessage]):
        print(F"{message.message.last_hop.name} => {node.name} (hop: {message.message.hops})")
