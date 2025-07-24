from dataclasses import dataclass
from typing import TYPE_CHECKING

from meshtastic_sim import Message

if TYPE_CHECKING:
    from simple_node import SimpleNode


@dataclass
class SimpleMessage(Message):
    source: "SimpleNode"
    target: "SimpleNode"
    last_hop: "SimpleNode"
    hops: int
    id: int
