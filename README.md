# RaceDash Balancer

> Telemetry relay for F1 25 — one source, multiple screens.

RaceDash Balancer is a lightweight Python app that sits between your F1 25 game and your devices. It listens for the UDP telemetry stream broadcast by the game and forwards every packet — in real time — to as many destinations as you configure.

Built for sim racers who run **RaceDash** on multiple devices simultaneously (iPad on the wheel stand, iPhone on the desk, whatever your setup is). No data loss, no configuration nightmare, just plug and race.

---

## How it works

```
F1 25 (PC/Console)
      │
      │  UDP telemetry (port 20777)
      ▼
RaceDash Balancer
      │
      ├──▶ iPad  (RaceDash)
      └──▶ iPhone (RaceDash)
```

The game sends telemetry to a single IP. Balancer receives it and fans it out to every device on your local network, with no perceptible delay.

---

## Features

- Real-time UDP relay with sub-millisecond overhead
- Supports any number of destination devices
- Configurable via `config.yaml` or command-line flags
- Live stats: packets/s, bytes/s, per-device loss rate
- Graceful shutdown — no dropped packets on exit

---

## Requirements

- Python 3.10+
- F1 25 with UDP telemetry output enabled
- Devices running [RaceDash](https://www.racedash.app) on the same local network

---

## Quick start

```bash
# Install dependencies
pip install -r requirements.txt

# Or use uv to install it!

# Edit your device IPs
cp config.example.yaml config.yaml

# Run
python -m racedash_balancer
```

---