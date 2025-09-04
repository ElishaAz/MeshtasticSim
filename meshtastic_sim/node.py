from abc import ABC, abstractmethod
from enum import Enum
from typing import TypeVar, Generic

from .message import SendingMessage, ReceivingMessage

S = TypeVar('S', bound=SendingMessage)
R = TypeVar('R', bound=ReceivingMessage)


class RadioState(Enum):
    LISTENING = 0
    RECEIVING = 1
    SENDING = 2


class Node(ABC, Generic[S, R]):
    def __init__(self, location: tuple[float, float] | None = None, radius: float | None = None):
        """
        Create a node.
        :param location: The location of the node (mostly for visualization).
        :param radius: The sending radius of the node (mostly for visualization).
        """
        self.location: tuple[float, float] = location
        self.radius: float = radius

    @abstractmethod
    def step(self, step: int, received: R | None, state: RadioState) -> S | None:
        """
        Do a single simulation step.
        :param step: The current simulation step number.
        :param received: A ReceivingMessage instance if one was received, None otherwise.
        :param state: The current state of the radio.
        :return: A SendingMessage if one is being sent, None otherwise.
        """
        pass
