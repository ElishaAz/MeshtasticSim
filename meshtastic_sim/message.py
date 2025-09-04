from typing import TypeVar, Generic


class Message:
    """
    A message that can be sent by a node.
    """
    pass


M = TypeVar('M', bound=Message)


class SendingMessage(Generic[M]):
    """
    A message as it is sent by a node.
    Can include e.g. TX power and other variables about how the message is sent (that can influence if the message is received or not)
    """

    def __init__(self, message: M):
        self.message: M = message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.message})"

    def __str__(self) -> str:
        return self.__repr__()


class ReceivingMessage(Generic[M]):
    """
    A message as it is received by a node.
    Can include e.g. RSSI and other statistics about how the message was received.
    """

    def __init__(self, message: M):
        self.message: M = message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.message})"

    def __str__(self) -> str:
        return self.__repr__()
