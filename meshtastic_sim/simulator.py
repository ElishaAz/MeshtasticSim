import itertools
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from .environment import Environment
from .logger import Logger
from .message import SendingMessage, ReceivingMessage
from .node import Node, RadioState

E = TypeVar('E', bound=Environment)
N = TypeVar('N', bound=Node)
L = TypeVar('L', bound=Logger)
S = TypeVar('S', bound=SendingMessage)
R = TypeVar('R', bound=ReceivingMessage)


@dataclass
class SimulatorState(Generic[N, S, R]):
    step: int = 0
    node_radio_states: dict[N, RadioState] = field(default_factory=dict)  # node -> radio state
    sent_messages: dict[N, tuple[S, int]] = field(default_factory=dict)  # node -> (message, step sent)
    receiving_messages: dict[N, N] = field(default_factory=dict)  # node -> sender node


class Simulator(Generic[E, N, L, S, R]):
    def __init__(self, nodes: list[N], environment: E, logger: L | None = None):
        """
        Create a simulator.
        :param nodes: A list of Nodes.
        :param environment: An Environment.
        """
        self.nodes: list[N] = nodes
        self.environment: E = environment
        self.logger: L = logger

        self.state: SimulatorState[N, S, R] = SimulatorState()

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

        self.environment.pre_step(self.state.step)

        received_messages: dict[N, R] = dict()
        sent_now_messages: dict[N, S] = dict()

        for node in self.nodes:
            if self.state.node_radio_states.get(node, RadioState.LISTENING) == RadioState.RECEIVING:
                receiving_from = self.state.receiving_messages[node]
                interference = self.environment.interfering(
                    self.state.step, node, receiving_from, self.state.sent_messages)

                if interference:
                    self.state.node_radio_states[node] = RadioState.LISTENING
                    del self.state.receiving_messages[node]

                    if self.logger is not None:
                        message, step_sent = self.state.sent_messages[receiving_from]
                        self.logger.interference(self.state.step, node, receiving_from, message, step_sent)

        for node in self.nodes:
            if self.state.node_radio_states.get(node, RadioState.LISTENING) == RadioState.SENDING:
                message, sent_step = self.state.sent_messages[node]
                finished_sending = self.environment.finished_sending(
                    self.state.step, node, message, sent_step)

                if finished_sending:
                    self.logger.finished_sending(self.state.step, node, message, sent_step)
                    self.state.node_radio_states[node] = RadioState.LISTENING

                    for receiver, sender in self.state.receiving_messages.items():
                        if sender == node:
                            received_message = self.environment.receives(
                                self.state.step, receiver, sender, message, sent_step)

                            if received_message is not None:
                                received_messages[receiver] = received_message

                            self.state.node_radio_states[receiver] = RadioState.LISTENING

                    del self.state.sent_messages[node]

        for node in self.nodes:
            received_message = received_messages.get(node, None)

            if received_message is not None and self.logger is not None:
                self.logger.message_received(self.state.step, node, received_message)

            outgoing_message = node.step(self.state.step, received_message,
                                         self.state.node_radio_states.get(node, RadioState.LISTENING))

            # TODO: Add a can_send check to the Environment

            if outgoing_message is not None:
                self.state.node_radio_states[node] = RadioState.SENDING
                sent_now_messages[node] = outgoing_message
                self.state.sent_messages[node] = (outgoing_message, self.state.step)
                if self.logger is not None:
                    self.logger.started_sending(self.state.step, node, outgoing_message)

        for node in self.nodes:
            if self.state.node_radio_states.get(node, RadioState.LISTENING) == RadioState.LISTENING:
                sender_node = self.environment.receiving(self.state.step, node, sent_now_messages,
                                                         self.state.sent_messages)
                if sender_node is not None:
                    self.state.node_radio_states[node] = RadioState.RECEIVING
                    self.state.receiving_messages[node] = sender_node

        self.environment.post_step(self.state.step)

        if self.logger is not None:
            self.logger.post_step(self.state.step)

        self.state.step += 1

        return self.state
