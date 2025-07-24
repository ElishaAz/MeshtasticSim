import itertools
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from .environment import Environment
from .logger import Logger
from .message import ReceivingMessageType, SendingMessageType
from .node import Node

E = TypeVar('E', bound=Environment)
N = TypeVar('N', bound=Node)
L = TypeVar('L', bound=Logger)


@dataclass
class SimulatorState:
    step: int = 0
    sent_messages: dict[Node, SendingMessageType | None] = field(default_factory=dict)
    received_messages: dict[Node, ReceivingMessageType | None] = field(default_factory=dict)


class Simulator(Generic[E, N, L]):
    def __init__(self, nodes: list[N], environment: E, logger: L | None = None):
        """
        Create a simulator.
        :param nodes: A list of Nodes.
        :param environment: An Environment.
        """
        self.nodes: list[N] = nodes
        self.environment: E = environment
        self.logger: L = logger

        self.state = SimulatorState()

        if self.logger is not None:
            for node in nodes:
                self.logger.node_added(-1, node)

    def start(self):
        self.state = SimulatorState()
        self.environment.start(self)

    def main(self, steps: int = -1) -> None:
        """
        Run the simulation.
        :param steps: The number of simulation steps to run. -1 for infinity.
        """
        iterator = itertools.count() if steps == -1 else range(steps)
        for _ in iterator:
            self.do_step()

    def add_node(self, node: N) -> None:
        self.nodes.append(node)
        if self.logger is not None:
            self.logger.node_added(self.state.step, node)

    def remove_node(self, node: Node) -> None:
        if node in self.nodes:
            self.nodes.remove(node)

            if self.logger is not None:
                self.logger.node_removed(self.state.step, node)

    def do_step(self) -> SimulatorState:
        """
        Do a single step of the simulation.
        :param step: The current step number.
        :param state: The internal state of the simulator.
        :return: The internal state of the simulator.
        """

        if self.logger is not None:
            self.logger.pre_step(self.state.step)

        outgoing_messages: dict[N, SendingMessageType] = dict()
        for node in self.nodes:
            incoming_message = self.state.received_messages.get(node, None)

            if incoming_message is not None and self.logger is not None:
                self.logger.message_received(self.state.step, node, incoming_message)

            outgoing_message = node.step(self.state.step, incoming_message)

            if outgoing_message is not None:
                outgoing_messages[node] = outgoing_message
                if self.logger is not None:
                    self.logger.message_sent(self.state.step, node, outgoing_message)

        self.state.sent_messages = outgoing_messages

        incoming_messages = self._send_messages(self.state.step, outgoing_messages)

        self.state.received_messages = incoming_messages

        if self.logger is not None:
            self.logger.post_step(self.state.step)

        self.state.step += 1

        return self.state

    def _send_messages(self, step: int,
                       outgoing_messages: dict[N, SendingMessageType]) -> dict[N, ReceivingMessageType | None]:
        """
        Calculates if sent messages are received, and by whom.
        :param step: The current simulation step.
        :param outgoing_messages: The messages sent by each node, node -> message sent.
        :return: The message received by each node, node -> message received.
        """
        incoming_messages: dict[N, ReceivingMessageType | None] = dict()

        for sender, message in outgoing_messages.items():
            for receiver in self.nodes:
                if sender == receiver:
                    continue

                received_message = self.environment.receives(step, sender, receiver, message)
                if received_message is not None:
                    if receiver in incoming_messages:
                        # The two (or more) messages interfere with each other, so no message is received TODO: make this a function in Environment.
                        # incoming_messages[receiver] = None
                        pass
                    else:
                        incoming_messages[receiver] = received_message

        return incoming_messages
