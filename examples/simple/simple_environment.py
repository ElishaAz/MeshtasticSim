import math
import random

from examples.simple.simple_message import SimpleMessage
from meshtastic_sim import Environment, SendingMessage, ReceivingMessage, Simulator
from simple_logger import SimpleLogger
from simple_node import SimpleNode

N = SimpleNode
S = SendingMessage[SimpleMessage]
R = ReceivingMessage[SimpleMessage]


class SimpleEnvironment(Environment[N, S, R]):
    def __init__(self, send_time: int = 10):
        self.send_time = send_time

    def start(self, simulator: Simulator[
        "SimpleEnvironment", N, SimpleLogger, S, R]) -> None:
        node = simulator.nodes[0]
        node.send_message(
            SimpleMessage(node, simulator.nodes[len(simulator.nodes) - 1], node, 10, random.randint(0, 2 ** 32 - 1)))

    def _in_range(self, sender: N, receiver: N) -> bool:
        sender_pos = sender.location
        receiver_pos = receiver.location
        diff = [abs(sender_pos[0] - receiver_pos[0]), abs(sender_pos[1] - receiver_pos[1])]
        distance = math.sqrt((diff[0]) ** 2 + (diff[1]) ** 2)
        return distance < sender.radius

    def receiving(self, step: int, receiver: N, sent_now_messages: dict[N, S],
                  sent_messages: dict[N, tuple[S, int]]) -> N | None:
        for sender, message in sent_now_messages.items():
            if self._in_range(sender, receiver):
                return sender
        return None

    def interfering(self, step: int, receiver: N, receiving_from: N, sent_messages: dict[N, tuple[S, int]]) -> bool:
        return False

    def finished_sending(self, step: int, sender: N, message: S, sent_step: int) -> bool:
        return step >= sent_step + self.send_time

    def receives(self, step: int, receiver: N, sender: N, message: S, sent_step: int) -> R | None:
        if self._in_range(sender, receiver):
            return ReceivingMessage(message.message)
        else:
            return None
