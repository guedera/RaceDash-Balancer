import socket
import time
from collections.abc import Callable

from .stats import Stats

_RETRY_DELAYS = [1, 2, 5, 10, 30]


class UDPListener:
    def __init__(self, port: int, on_packet: Callable[[bytes], None], stats: Stats) -> None:
        self.port = port
        self.on_packet = on_packet
        self.stats = stats
        self._sock: socket.socket | None = None
        self._running = False

    def start(self) -> None:
        self._running = True
        attempt = 0

        while self._running:
            try:
                self._bind()
                attempt = 0
                self._recv_loop()
            except OSError as e:
                if not self._running:
                    break
                delay = _RETRY_DELAYS[min(attempt, len(_RETRY_DELAYS) - 1)]
                print(f"\nSocket error: {e}. Retrying in {delay}s...")
                attempt += 1
                time.sleep(delay)

    def _bind(self) -> None:
        self._close_sock()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(("0.0.0.0", self.port))

    def _recv_loop(self) -> None:
        while self._running:
            data, _ = self._sock.recvfrom(65535)
            self.stats.record_recv(len(data))
            self.on_packet(data)

    def close(self) -> None:
        self._running = False
        self._close_sock()

    def _close_sock(self) -> None:
        if self._sock:
            self._sock.close()
            self._sock = None
