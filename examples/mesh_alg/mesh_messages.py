from dataclasses import dataclass
from typing import Any

from meshtastic_sim import Message, SendingMessage, ReceivingMessage


@dataclass
class HeaderFlags:
    hop_limit: int  # 3 bits
    want_ack: bool
    via_mqtt: bool  # Packet came via MQTT
    hop_start: int  # 3 bits. Original Hop Limit


@dataclass
class MeshMessage(Message):
    ####### HEADER #######
    destination: int  # Packet Header: Destination. The destination's unique NodeID. 0xFFFFFFFF for broadcast.
    sender: int  # Packet Header: Sender. The sender's unique NodeID.
    packet_id: int  # Packet Header: The sending node's unique packet ID for this packet.
    flags: HeaderFlags
    channel_hash: int  # 1 byte. Packet Header: Channel hash. Used as hint for decryption for the receiver.
    next_hop: int  # 1 byte. Packet Header: Next-hop used for relaying.
    relay_node: int  # 1 byte. Packet Header: Relay node of the current transmission.

    ####### PAYLOAD #######
    payload: Any  # Max 237 bytes. Actual packet data. Unused bytes are not transmitted.


@dataclass
class MeshSendingMessage(SendingMessage[MeshMessage]):
    tx_power: float  # Transmission power in mW.
    message: MeshMessage  # The actual message being sent.


@dataclass
class MeshReceivingMessage(ReceivingMessage[MeshMessage]):
    rssi: float  # Received Signal Strength Indicator in mW.
    message: MeshMessage  # The actual message received.
