from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

from .message import ReceivingMessage, SendingMessage
from .node import Node

if TYPE_CHECKING:
    # noinspection PyUnusedImports
    from .simulator import Simulator

N = TypeVar('N', bound=Node)
S = TypeVar('S', bound=SendingMessage)
R = TypeVar('R', bound=ReceivingMessage)


class Environment(ABC, Generic[N, S, R]):
    """
    A simulation environment.
    """

    @abstractmethod
    def start(self, simulator: "Simulator") -> None:
        pass

    @abstractmethod
    def receiving(self, step: int, receiver: N,
                  sent_now_messages: dict[N, S], sent_messages: dict[N, tuple[S, int]]) -> N | None:
        """
        Determines if a node receives a message from any sending node.
        :param step: The current simulation step number.
        :param receiver: The node that may receive the message.
        :param sent_now_messages: A dictionary of all messages that started sending in the current step. (sender -> message)
        :param sent_messages: A dictionary of all messages that are currently being sent. (sender -> (message, step sent))
        :return: The sending node if a message is being received, None otherwise.
        """
        pass

    @abstractmethod
    def interfering(self, step: int, receiver: N, receiving_from: N, sent_messages: dict[N, tuple[S, int]]) -> bool:
        """
        Determines if a node is experiencing interference from other sending nodes.
        :param step: The current simulation step number.
        :param receiver: The node that may be experiencing interference.
        :param receiving_from: The node that is currently sending a message to the receiver.
        :param sent_messages: A dictionary of all messages that are currently being sent. (sender -> (message, step sent))
        :return: True if the node is experiencing interference (and will therefore not receive the message from `receiving_from`), False otherwise.
        """
        pass

    @abstractmethod
    def finished_sending(self, step: int, sender: N, message: S, sent_step: int) -> bool:
        """
        Determines if a node has finished sending a message.
        :param step: The current simulation step number.
        :param sender: The sending node.
        :param message: The message being sent.
        :param sent_step: The step number when the message started being sent.
        :return: True if the node has finished sending the message, False otherwise.
        """
        pass

    @abstractmethod
    def receives(self, step: int, receiver: N, sender: N, message: S, sent_step: int) -> R | None:
        """
        Determines if a node receives a message from another node.
        :param step: The current simulation step number.
        :param sender: The sending node.
        :param receiver: The receiving node.
        :param message: The message being sent.
        :param sent_step: The step number when the message started being sent.
        :return: A ReceivingMessage instance if the message was received, None otherwise.
        """
        pass

    def pre_step(self, step: int):
        """
        Called before each simulation step.
        :param step: The current simulation step number.
        """
        pass

    def post_step(self, step: int):
        """
        Called after each simulation step.
        :param step: The current simulation step number.
        """
        pass
