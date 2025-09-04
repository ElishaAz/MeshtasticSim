from abc import ABC, abstractmethod
from typing import TypeVar

from .message import SendingMessage, ReceivingMessage
from .node import Node

S = TypeVar('S', bound=SendingMessage)
R = TypeVar('R', bound=ReceivingMessage)


class Logger(ABC):

    @abstractmethod
    def pre_step(self, step: int) -> None:
        """
        Called before every simulation step.
        :param step: The current simulation step number.
        """
        pass

    @abstractmethod
    def post_step(self, step: int) -> None:
        """
        Called after every simulation step.
        :param step: The current simulation step number.
        """
        pass

    @abstractmethod
    def node_added(self, step: int, node: Node) -> None:
        """
        Called when a node is added to the simulation.
        :param step: The current simulation step number.
        :param node: The node that was added.
        """
        pass

    @abstractmethod
    def node_removed(self, step: int, node: Node) -> None:
        """
        Called when a node is removed from the simulation.
        :param step: The current simulation step number.
        :param node: The node that was removed.
        """
        pass

    @abstractmethod
    def started_sending(self, step: int, node: Node, message: S) -> None:
        """
        Called when a node starts sending a message.
        :param step: The current simulation step number.
        :param node: The node that started sending the message.
        :param message: The message that was sent.
        """
        pass

    @abstractmethod
    def interference(self, step: int, receiver: Node, sender: Node, message: S, step_sent: int) -> None:
        """
        Called when a node experiences interference while receiving a message.
        :param step: The current simulation step number.
        :param receiver: The node experiencing interference.
        :param sender: The node that is sending the message that experienced interference.
        :param message: The message being sen that experienced interference.
        :param step_sent: The step number when the message started being sent.
        """
        pass

    @abstractmethod
    def finished_sending(self, step: int, node: Node, message: S, sent_step: int) -> None:
        """
        Called when a node finishes sending a message.
        :param step: The current simulation step number.
        :param node: The node that finished sending the message.
        :param message: The message that was sent.
        :param sent_step: The step number when the message started being sent.
        """
        pass

    @abstractmethod
    def message_received(self, step: int, node: Node, message: R):
        """
        Called when a node receives a message.
        :param step: The current simulation step number.
        :param node: The node that received the message.
        :param message: The message that was received.
        """
        pass
