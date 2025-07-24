from typing import Any

from meshtastic_sim import Logger
from meshtastic_sim.message import ReceivingMessage, SendingMessage
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
        pass

    def message_sent(self, step: int, node: SimpleNode, message: SendingMessage[SimpleMessage]):
        pass

    def message_received(self, step: int, node: SimpleNode, message: ReceivingMessage[SimpleMessage]):
        print(F"{message.message.last_hop.name} => {node.name} (hop: {message.message.hops})")
