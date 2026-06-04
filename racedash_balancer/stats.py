import threading
import time
from dataclasses import dataclass, field


@dataclass
class Stats:
    packets_recv: int = 0
    bytes_recv: int = 0
    packets_sent: dict[str, int] = field(default_factory=dict)
    errors: dict[str, int] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def record_recv(self, nbytes: int) -> None:
        with self._lock:
            self.packets_recv += 1
            self.bytes_recv += nbytes

    def record_sent(self, name: str) -> None:
        with self._lock:
            self.packets_sent[name] = self.packets_sent.get(name, 0) + 1

    def record_error(self, name: str) -> None:
        with self._lock:
            self.errors[name] = self.errors.get(name, 0) + 1

    def snapshot(self) -> "Stats":
        with self._lock:
            return Stats(
                packets_recv=self.packets_recv,
                bytes_recv=self.bytes_recv,
                packets_sent=dict(self.packets_sent),
                errors=dict(self.errors),
            )


def _format_bytes(n: int) -> str:
    if n >= 1024 * 1024:
        return f"{n / (1024 * 1024):.1f} MB/s"
    if n >= 1024:
        return f"{n / 1024:.1f} KB/s"
    return f"{n} B/s"


def start_printer(stats: Stats, interval: float = 1.0) -> threading.Thread:
    prev = stats.snapshot()

    def loop() -> None:
        nonlocal prev
        while True:
            time.sleep(interval)
            cur = stats.snapshot()

            pkt_rate = cur.packets_recv - prev.packets_recv
            byte_rate = cur.bytes_recv - prev.bytes_recv

            parts = [f"recv {pkt_rate:>4} pkt/s  {_format_bytes(byte_rate):>12}"]
            for name in cur.packets_sent:
                sent = cur.packets_sent[name] - prev.packets_sent.get(name, 0)
                err = cur.errors.get(name, 0)
                parts.append(f"{name}: {sent:>4} pkt/s  {err} err")

            line = "  |  ".join(parts)
            print(f"\r{line:<80}", end="", flush=True)

            prev = cur

    t = threading.Thread(target=loop, daemon=True)
    t.start()
    return t
