import socket

from .config import Destination


class UDPForwarder:
    def __init__(self, destinations: list[Destination]) -> None:
        self.destinations = destinations
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def forward(self, data: bytes) -> None:
        for dest in self.destinations:
            try:
                self._sock.sendto(data, (dest.ip, dest.port))
            except OSError:
                pass

    def close(self) -> None:
        self._sock.close()
