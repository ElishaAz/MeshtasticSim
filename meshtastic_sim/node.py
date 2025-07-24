from abc import ABC, abstractmethod

from .message import ReceivingMessageType, SendingMessageType


class Node(ABC):
    def __init__(self, location: tuple[float, float] | None = None, radius: float | None = None):
        """
        Create a node.
        :param location: The location of the node (mostly for visualization).
        :param radius: The sending radius of the node (mostly for visualization).
        """
        self.location: tuple[float, float] = location
        self.radius: float = radius

    @abstractmethod
    def step(self, step: int, received: ReceivingMessageType | None) -> SendingMessageType | None:
        """
        Do a single simulation step.
        :param step: The current simulation step number.
        :param received: A ReceivingMessage instance if one was received, None otherwise.
        :return: A SendingMessage if one is being sent, None otherwise.
        """
        pass
