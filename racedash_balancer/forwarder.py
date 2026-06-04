import socket

from .config import Destination
from .stats import Stats


class UDPForwarder:
    def __init__(self, destinations: list[Destination], stats: Stats) -> None:
        self.destinations = destinations
        self.stats = stats
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def forward(self, data: bytes) -> None:
        for dest in self.destinations:
            try:
                self._sock.sendto(data, (dest.ip, dest.port))
                self.stats.record_sent(dest.name)
            except OSError:
                self.stats.record_error(dest.name)

    def close(self) -> None:
        self._sock.close()
