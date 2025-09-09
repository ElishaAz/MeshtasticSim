from examples.mesh_alg.mesh_messages import MeshSendingMessage, MeshReceivingMessage, Ack, Nak, HeaderFlags, MeshMessage
from examples.mesh_alg.mesh_node_layer1 import MeshNodeLayer1
from examples.mesh_alg.utils import random_packet_id, ACK_TIMEOUT, MAX_RETRIES

S = MeshSendingMessage
R = MeshReceivingMessage


class MeshNodeLayer2(MeshNodeLayer1):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.queued_messages: dict[int, tuple[MeshMessage, int]] = dict()  # Message id => (Message, retries)

    def _send_message_layer_2(self, message: MeshMessage):
        self.queued_messages[message.packet_id] = (message, 0)
        self._send_message_layer_1(message)

    def _received_message_layer_2(self, step: int, message: R, already_received: bool):
        do_send_ack = False
        received_message = message.message
        if received_message.destination == self.id and not already_received:
            if isinstance(received_message.payload, (Ack, Nak)):
                ack = received_message.payload
                exists = False
                for queued_message, _ in self.queued_messages.values():
                    if ack.packet_id == queued_message.packet_id:
                        exists = True
                        break
                if exists:
                    # We got an ack, no need to retransmit
                    del self.queued_messages[ack.packet_id]
                    self._got_ack_layer_3(isinstance(received_message.payload, Ack), ack.packet_id)
            elif received_message.flags.want_ack:
                # Send an Ack
                do_send_ack = True

        messages_to_remove: list[int] = list()
        is_ack = isinstance(received_message.payload, (Ack, Nak))
        for queued_message, _ in self.queued_messages.values():
            if received_message.packet_id == queued_message.packet_id or (  # Someone heard us and is relaying
                    is_ack and received_message.payload.packet_id == queued_message.packet_id):  # Someone responded with an ack / nak
                messages_to_remove.append(queued_message.packet_id)  # No need to retransmit
        for m in messages_to_remove:
            del self.queued_messages[m]

        if not already_received:
            self._received_message_layer_3(step, message)

        if do_send_ack:
            # Need sto happen after _received_message_layer_3
            self._send_ack(True, received_message)

    def _received_message_layer_3(self, step: int, message: R):
        pass

    def _got_ack_layer_3(self, ack: bool, packet_id: int) -> None:
        pass

    def _send_ack(self, is_ack: bool, message: MeshMessage):
        flags = HeaderFlags(message.flags.hop_limit, False, False,
                            message.flags.hop_limit)
        self._send_message_layer_2(
            MeshMessage(destination=message.sender, sender=self.id, packet_id=random_packet_id(), flags=flags,
                        channel_hash=0,
                        next_hop=message.relay_node, relay_node=self.relay_id,
                        payload=Ack(message.packet_id) if is_ack else Nak(message.packet_id))
        )

    def _step(self, step: int) -> None:
        messages_to_remove: list[int] = list()
        messages_to_send_nak: list[MeshMessage] = list()
        for queued_message, retries in self.queued_messages.values():
            if queued_message.packet_id in self.sent_messages:
                if step - self.sent_messages[queued_message.packet_id] >= ACK_TIMEOUT:
                    if retries >= MAX_RETRIES:
                        packet_id = queued_message.packet_id
                        messages_to_remove.append(queued_message.packet_id)  # Remove this message from the queue

                        if queued_message.sender != self.id and queued_message.flags.want_ack:  # Was not sent by us
                            # Send a Nak
                            messages_to_send_nak.append(queued_message)

                        self._got_ack_layer_3(False, packet_id)
                    else:
                        # Resend the message
                        self._send_message_layer_1(queued_message)
                        self.queued_messages[queued_message.packet_id] = (queued_message, retries + 1)
        for m in messages_to_remove:
            del self.queued_messages[m]
        for m in messages_to_send_nak:
            self._send_ack(False, m)
