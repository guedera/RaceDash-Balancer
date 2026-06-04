import argparse
from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class Destination:
    name: str
    ip: str
    port: int


@dataclass
class Config:
    listen_port: int
    destinations: list[Destination] = field(default_factory=list)


def load_config() -> Config:
    parser = argparse.ArgumentParser(description="RaceDash Balancer — UDP telemetry relay for F1 25")
    parser.add_argument("--config", type=Path, default=Path("config.yaml"), help="Path to config file")
    parser.add_argument("--port", type=int, help="Override listen port")
    args = parser.parse_args()

    if not args.config.exists():
        parser.error(f"Config file not found: {args.config}\nCopy config.example.yaml to config.yaml and edit it.")

    with args.config.open() as f:
        raw = yaml.safe_load(f)

    listen_port = args.port or raw.get("listen_port", 20777)

    destinations = [
        Destination(name=d["name"], ip=d["ip"], port=d.get("port", 20777))
        for d in raw.get("destinations", [])
    ]

    if not destinations:
        parser.error("No destinations configured. Add at least one device to config.yaml.")

    return Config(listen_port=listen_port, destinations=destinations)
