import signal
import sys

from .config import load_config


def main() -> None:
    config = load_config()

    print(f"RaceDash Balancer — listening on port {config.listen_port}")
    print(f"Forwarding to {len(config.destinations)} device(s):")
    for dest in config.destinations:
        print(f"  {dest.name}: {dest.ip}:{dest.port}")
    print("\nPress Ctrl+C to stop.\n")

    def shutdown(sig, frame):
        print("\nShutting down...")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    signal.pause()


if __name__ == "__main__":
    main()
