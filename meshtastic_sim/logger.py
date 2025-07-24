from abc import ABC, abstractmethod

from .message import SendingMessageType, ReceivingMessageType
from .node import Node


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
        pass

    @abstractmethod
    def node_removed(self, step: int, node: Node) -> None:
        pass

    @abstractmethod
    def message_sent(self, step: int, node: Node, message: SendingMessageType) -> None:
        pass

    @abstractmethod
    def message_received(self, step: int, node: Node, message: ReceivingMessageType):
        pass
