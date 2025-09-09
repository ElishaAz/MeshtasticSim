from queue import Queue

from examples.mesh_alg.mesh_messages import MeshMessage, MeshSendingMessage, MeshReceivingMessage
from examples.mesh_alg.mesh_node_layer0 import MeshNodeLayer0
from meshtastic_sim import RadioState

S = MeshSendingMessage
R = MeshReceivingMessage


class MeshNodeLayer1(MeshNodeLayer0):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_received_message_ids = set()
        self.sent_messages: dict[int, int] = dict()  # Message id => step sent

        self._queued_messages: Queue[MeshMessage] = Queue()

    def _send_message_layer_1(self, message: MeshMessage):
        self._queued_messages.put(message)

    def _received_message_layer_2(self, step: int, message: R, already_received: bool):
        pass

    def _step(self, step: int) -> None:
        pass

    def step(self, step: int, received: R | None, radio_state: RadioState) -> S | None:
        if received is not None:
            self._received_message_layer_2(step, received, received.message.packet_id in self.all_received_message_ids)
            self.all_received_message_ids.add(received.message.packet_id)

        self._step(step)

        if radio_state == RadioState.LISTENING and not self._queued_messages.empty():
            if self.environment.do_cad(self):
                message = self._queued_messages.get()
                message_sending = MeshSendingMessage(self.tx_power, message)
                self.sent_messages[message.packet_id] = step
                self.all_received_message_ids.add(message.packet_id)  # Ignore messages that we sent
                return message_sending

        return None
