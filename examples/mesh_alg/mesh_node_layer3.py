from dataclasses import replace
from typing import Callable

from examples.mesh_alg.mesh_messages import MeshSendingMessage, MeshReceivingMessage, MeshMessage, HeaderFlags, Nak, Ack
from examples.mesh_alg.mesh_node_layer2 import MeshNodeLayer2
from examples.mesh_alg.utils import MAX_RETRIES, send_step_for_message, random_packet_id

S = MeshSendingMessage
R = MeshReceivingMessage


class MeshNodeLayer3(MeshNodeLayer2):
    def __init__(self, *args, message_received: Callable[[MeshMessage], None] = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.message_received: Callable[[MeshMessage], None] | None = message_received
        self.relayed_messages: list[tuple[MeshMessage, int]] = list()
        self.next_hops: dict[int, int] = dict()  # node => relay

    def send_message(self, message: MeshMessage):
        self._send_message_layer_2(
            replace(message, relay_node=self.relay_id, next_hop=self.next_hops.get(message.destination, 0)))

    def _received_message_layer_3(self, step: int, message: R):
        received_message = message.message

        # Update next_hop dict
        if received_message.relay_node != 0:
            self.next_hops[received_message.sender] = received_message.relay_node

        remove_item = None
        for relay_message, send_step in self.relayed_messages:
            if relay_message.packet_id == received_message.packet_id:
                remove_item = (relay_message, send_step)  # Someone already relayed the message
        if remove_item is not None:
            self.relayed_messages.remove(remove_item)

        if received_message.destination == self.id:
            # We got a message (sending Ack is done by Layer 2)
            if self.message_received is not None:
                self.message_received(received_message)
        else:
            if received_message.next_hop == 0 or received_message.next_hop == self.relay_id:
                # Relay the message
                send_step = send_step_for_message(step, self, message)  # Wait a bit, depending on snr
                print("snr", message.snr, send_step - step)
                next_hop = self.next_hops.get(received_message.destination, 0)
                self.relayed_messages.append(
                    (replace(received_message, next_hop=next_hop, relay_node=self.relay_id), send_step))

    def _got_ack_layer_3(self, ack: bool, packet_id: int) -> None:
        pass

    def _send_ack(self, is_ack: bool, message: MeshMessage):
        flags = HeaderFlags(message.flags.hop_limit, False, False,
                            message.flags.hop_limit)
        self._send_message_layer_2(
            MeshMessage(destination=message.sender, sender=self.id, packet_id=random_packet_id(), flags=flags,
                        channel_hash=0,
                        next_hop=self.next_hops.get(message.sender, 0), relay_node=self.relay_id,
                        payload=Ack(message.packet_id) if is_ack else Nak(message.packet_id))
        )

    def _step(self, step: int) -> None:
        for queued_message, retries in self.queued_messages.values():
            if retries == MAX_RETRIES - 1:  # Last retry
                # Fall back to managed flooding
                if queued_message.next_hop in self.next_hops:
                    del self.next_hops[queued_message.next_hop]  # Remove from dict, not accessible anymore
                self.queued_messages[queued_message.packet_id] = (replace(queued_message, next_hop=0), retries)

        messages_to_remove = list()
        for relay_message, send_step in self.relayed_messages:
            if send_step <= step:
                self._send_message_layer_2(relay_message)
                messages_to_remove.append((relay_message, send_step))
        for message in messages_to_remove:
            self.relayed_messages.remove(message)

        super()._step(step)
