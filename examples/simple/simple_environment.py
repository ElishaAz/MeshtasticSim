import math
import random

from examples.simple.simple_message import SimpleMessage
from meshtastic_sim import Environment, Node, SendingMessage, ReceivingMessage, Simulator
from simple_logger import SimpleLogger
from simple_node import SimpleNode


class SimpleEnvironment(Environment):
    def __init__(self):
        pass

    def start(self, simulator: Simulator["SimpleEnvironment", SimpleNode, SimpleLogger]):
        node = simulator.nodes[0]
        node.send_message(
            SimpleMessage(node, simulator.nodes[len(simulator.nodes) - 1], node, 10, random.randint(0, 2 ** 32 - 1)))

    def receives(self, step: int, sender: Node, receiver: Node, message: SendingMessage) -> ReceivingMessage | None:
        sender_pos = sender.location
        receiver_pos = receiver.location
        diff = [abs(sender_pos[0] - receiver_pos[0]), abs(sender_pos[1] - receiver_pos[1])]
        distance = math.sqrt((diff[0]) ** 2 + (diff[1]) ** 2)
        if distance < sender.radius:
            return ReceivingMessage(message.message)
        else:
            return None
