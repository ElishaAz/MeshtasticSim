from typing import Optional

from meshtastic_sim import Node, ReceivingMessage, SendingMessage
from simple_message import SimpleMessage


class SimpleNode(Node):
    def __init__(self, name: str, location: tuple[float, float], radius: float):
        super().__init__(location, radius)
        self.name = name
        self.message = None

        self.received_messages = set()

    def send_message(self, message: SimpleMessage):
        self.message = message

    def step(self, step: int, received: Optional[ReceivingMessage[SimpleMessage]]) -> Optional[
        SendingMessage[SimpleMessage]]:
        if self.message is not None:
            message: SendingMessage[SimpleMessage] = SendingMessage(self.message)
            self.received_messages.add(self.message.id)
            self.message = None
            return message
        if received is None:
            return None
        hops = received.message.hops - 1
        if hops < 0 or received.message.id in self.received_messages:
            return None

        self.received_messages.add(received.message.id)

        if received.message.target == self:
            print(F"Message received by target {self.name}. ID: {received.message.id}")
            return None

        message: SimpleMessage = SimpleMessage(received.message.source, received.message.target, self, hops,
                                               received.message.id)

        return SendingMessage(message)
