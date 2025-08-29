import math
import random
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # noinspection PyUnusedImports
    from examples.mesh_alg.mesh_node import MeshNode

BROADCAST_ID = 0xFFFFFFFF


def rssi_at_distance(tx_power: float, distance: float) -> float:
    """
    Calculate the Received Signal Strength Indicator (RSSI) at a given distance from the transmitter.

    :param tx_power: Transmission power in mW.
    :param distance: Distance from the transmitter in meters.
    :return: RSSI in mW.
    """
    if distance <= 0:
        return tx_power  # If distance is zero or negative, return full power

    # Simple path loss model: RSSI = Tx Power / (distance^2)
    rssi = tx_power / (distance ** 2)

    return max(rssi, 0)  # Ensure RSSI is not negative


def distance_at_rssi(tx_power: float, rssi: float) -> float:
    """
    Calculate the distance at which a given RSSI is received from a transmitter.

    :param tx_power: Transmission power in mW.
    :param rssi: Received Signal Strength Indicator in mW.
    :return: Distance in meters.
    """
    if rssi <= 0 or tx_power <= 0:
        return float('inf')  # If RSSI or Tx Power is zero or negative, return infinite distance

    # Simple path loss model: distance = sqrt(Tx Power / RSSI)
    distance = math.sqrt(tx_power / rssi)

    return distance


def distance_between(node: "MeshNode", other: "MeshNode") -> float:
    distance = node.location[0] - other.location[0], node.location[1] - other.location[1]
    distance = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
    return distance


def random_packet_id() -> int:
    return random.randint(0, BROADCAST_ID - 1)


class SendingState(Enum):
    NOT_SENDING = 0
    SENDING = 1
    FINISHED = 2
