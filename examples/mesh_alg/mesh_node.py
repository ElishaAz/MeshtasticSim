from typing import TYPE_CHECKING

from mesh_messages import MeshMessage, MeshSendingMessage, MeshReceivingMessage
from meshtastic_sim import Node
from utils import distance_at_rssi, SendingState

if TYPE_CHECKING:
    # noinspection PyUnusedImports
    from mesh_environment import MeshEnvironment


class MeshNode(Node):
    def __init__(self, name: str, location: tuple[float, float], tx_power: float, sensitivity: float,
                 environment: "MeshEnvironment"):
        radius = distance_at_rssi(tx_power, sensitivity)
        super().__init__(location, radius)
        self.name = name
        self.message: MeshMessage | None = None
        self.tx_power = tx_power
        self.sensitivity = sensitivity
        self.environment = environment

        self.message_sending = None

        self.received_messages = set()

    def send_message(self, message: MeshMessage):
        self.message = message

    def step(self, step: int, received: MeshReceivingMessage | None) -> MeshSendingMessage | None:
        is_sending = self.environment.is_sending(self)

        if is_sending == SendingState.SENDING:
            return None

        if is_sending == SendingState.FINISHED:
            return self.message_sending

        if self.message is not None:
            self.message_sending = MeshSendingMessage(self.tx_power, self.message)
            if self.environment.try_send(self):
                self.message = None

        # TODO

        return None
