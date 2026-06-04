import socket
from collections.abc import Callable

from .stats import Stats


class UDPListener:
    def __init__(self, port: int, on_packet: Callable[[bytes], None], stats: Stats) -> None:
        self.port = port
        self.on_packet = on_packet
        self.stats = stats
        self._sock: socket.socket | None = None

    def start(self) -> None:
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(("0.0.0.0", self.port))

        while True:
            data, _ = self._sock.recvfrom(65535)
            self.stats.record_recv(len(data))
            self.on_packet(data)

    def close(self) -> None:
        if self._sock:
            self._sock.close()
            self._sock = None
