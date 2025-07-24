from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from .message import SendingMessageType, ReceivingMessageType
from .node import Node

if TYPE_CHECKING:
    from .simulator import Simulator


class Environment(ABC):
    """
    A simulation environment.
    """

    @abstractmethod
    def start(self, simulator: "Simulator"):
        pass

    @abstractmethod
    def receives(self, step: int,
                 sender: Node, receiver: Node,
                 message: SendingMessageType) -> ReceivingMessageType | None:
        """
        Determines if a node receives a message from another node.
        :param step: The current simulation step number.
        :param sender: The sending node.
        :param receiver: The receiving node.
        :param message: The message being sent.
        :return: A ReceivingMessage instance if the message was received, None otherwise.
        """
        pass
