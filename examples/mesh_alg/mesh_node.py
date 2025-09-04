from typing import TYPE_CHECKING

from examples.mesh_alg.mesh_messages import HeaderFlags
from examples.mesh_alg.utils import distance_at_rssi, BROADCAST_ID, random_packet_id
from mesh_messages import MeshMessage, MeshSendingMessage, MeshReceivingMessage, Ack, Nak
from meshtastic_sim import Node, RadioState

if TYPE_CHECKING:
    # noinspection PyUnusedImports
    from mesh_environment import MeshEnvironment

S = MeshSendingMessage
R = MeshReceivingMessage

ACK_TIMEOUT = 10


class MeshNode(Node):
    def __init__(self, id: int, name: str, location: tuple[float, float],
                 tx_power: float, sensitivity: float, environment: "MeshEnvironment"):
        radius = distance_at_rssi(tx_power, sensitivity)
        super().__init__(location, radius)
        self.id = id
        self.name = name
        self.queued_message: MeshMessage | None = None
        self.queued_message_sent = False
        self.queued_message_sent_step = -1
        self.queued_message_got_ack = False
        self.tx_power = tx_power
        self.sensitivity = sensitivity
        self.environment = environment

        self.message_sending = None

        self.received_messages = set()

    def send_message(self, message: MeshMessage):
        if self.queued_message_sent and not self.queued_message_got_ack:
            return  # A message is currently being sent

        self.queued_message = message
        self.queued_message_sent = False

    def step(self, step: int, received: R | None, radio_state: RadioState) -> S | None:

        # Layer 2

        if received is not None:
            received_message = received.message
            if received_message.destination == BROADCAST_ID:
                pass  # TODO implement broadcast ACK
            elif received_message.destination == self.id:
                if isinstance(received_message.payload, Ack):
                    ack = received_message.payload
                    if ack.packet_id == self.queued_message.packet_id:
                        self.queued_message_got_ack = True
                elif isinstance(received_message.payload, Nak):
                    nak = received_message.payload
                    if nak.packet_id == self.queued_message.packet_id:
                        self.queued_message_got_ack = True
                else:
                    flags = HeaderFlags(received_message.flags.hop_start, False, False,
                                        received_message.flags.hop_start)
                    self.send_message(
                        MeshMessage(received_message.sender, self.id, random_packet_id(), flags, 0,
                                    received_message.relay_node, 0, Ack(received_message.packet_id))
                    )
            else:
                pass  # TODO implement relay

        if self.queued_message_sent and not self.queued_message_got_ack:
            if step - self.queued_message_sent_step >= ACK_TIMEOUT:
                # Resend the message
                self.queued_message_sent = False

        # Layer 1

        if (radio_state == RadioState.LISTENING and self.queued_message is not None
                and not self.queued_message_sent and not self.queued_message_got_ack):
            if self.environment.do_cad(self):
                self.message_sending = MeshSendingMessage(self.tx_power, self.queued_message)
                if self.environment.do_cad(self):
                    self.queued_message_sent = True
                    self.queued_message_sent_step = step

                    if not self.message_sending.message.flags.want_ack:
                        self.queued_message = None  # We do not want ACK, no need to keep a reference

                    return self.message_sending  # Send the message

        return None
