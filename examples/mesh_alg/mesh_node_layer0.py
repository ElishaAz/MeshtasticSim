from typing import TYPE_CHECKING

from examples.mesh_alg.utils import distance_at_rssi
from mesh_messages import MeshMessage, MeshSendingMessage, MeshReceivingMessage
from meshtastic_sim import Node

if TYPE_CHECKING:
    # noinspection PyUnusedImports
    from mesh_environment import MeshEnvironment

S = MeshSendingMessage
R = MeshReceivingMessage


class MeshNodeLayer0(Node):
    def __init__(self, id: int, name: str, location: tuple[float, float],
                 tx_power: float, sensitivity: float, environment: "MeshEnvironment"):
        radius = distance_at_rssi(tx_power, sensitivity)
        super().__init__(location, radius)
        self.id = id
        self.relay_id = id
        self.name = name

        self.tx_power = tx_power
        self.sensitivity = sensitivity
        self.environment = environment
