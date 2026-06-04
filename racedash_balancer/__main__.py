import signal
import sys

from .config import load_config
from .forwarder import UDPForwarder
from .listener import UDPListener
from .stats import Stats, start_printer


def main() -> None:
    config = load_config()

    print(f"RaceDash Balancer — listening on port {config.listen_port}")
    print(f"Forwarding to {len(config.destinations)} device(s):")
    for dest in config.destinations:
        print(f"  {dest.name}: {dest.ip}:{dest.port}")
    print("\nPress Ctrl+C to stop.\n")

    stats = Stats()
    forwarder = UDPForwarder(config.destinations, stats)
    listener = UDPListener(port=config.listen_port, on_packet=forwarder.forward, stats=stats)
    start_printer(stats)

    def shutdown(sig, frame):
        print("\nShutting down...")
        listener.close()
        forwarder.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    listener.start()


if __name__ == "__main__":
    main()
