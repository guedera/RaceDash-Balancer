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
RaceDash Balancer  ← running on your PC/Mac
      │
      ├──▶ iPad  (RaceDash)
      └──▶ iPhone (RaceDash)
```

The game sends telemetry to a single IP — the machine running this app. Balancer receives it and fans it out to every device on your local network, with no perceptible delay.

---

## Features

- Real-time UDP relay with sub-millisecond overhead
- Supports any number of destination devices
- Configurable via `config.yaml` or command-line flags
- Live stats: packets/s, bytes/s, per-device error rate
- Auto-reconnect on socket errors
- Graceful shutdown with Ctrl+C

---

## Requirements

- Python 3.12+
- F1 25 with UDP telemetry output enabled
- Devices running [RaceDash](https://www.racedash.app) on the same local network

---

## Step 1 — Find your IPs

You need three IP addresses, all on the same local Wi-Fi network.

**IP of the machine running this app (your PC/Mac)**

This is what you'll type into F1 25. To find it:

- **macOS:** System Settings → Network → Wi-Fi → Details → IP Address
- **Windows:** `ipconfig` in a terminal → look for `IPv4 Address` under your Wi-Fi adapter

Example: `192.168.1.50`

**IP of each RaceDash device (iPad, iPhone)**

On each device: Settings → Wi-Fi → tap your network name → IP Address.

Example: iPad `192.168.1.100`, iPhone `192.168.1.101`

---

## Step 2 — Configure F1 25

In the game, go to:

```
Main Menu → Settings → Telemetry Settings
```

| Setting | Value |
|---|---|
| UDP Telemetry | On |
| UDP Broadcast Mode | Off |
| UDP IP Address | IP of the machine running this app (e.g. `192.168.1.50`) |
| UDP Port | `20777` |
| UDP Send Rate | 60Hz (or your preference) |
| UDP Format | 2024 |

---

## Step 3 — Configure the app

Copy the example config and edit it:

```bash
cp config.example.yaml config.yaml
```

Fill in the IPs you collected in Step 1:

```yaml
listen_port: 20777   # must match the port set in F1 25

destinations:
  - name: iPad
    ip: 192.168.1.100  # IP of your iPad
    port: 20777        # port RaceDash listens on (default: 20777)
  - name: iPhone
    ip: 192.168.1.101  # IP of your iPhone
    port: 20777
```

You can add or remove destinations freely — one device, three devices, whatever your setup needs.

---

## Step 4 — Install and run

**With uv (recommended):**

```bash
uv sync
uv run python -m racedash_balancer
```

**With pip:**

```bash
pip install pyyaml
python -m racedash_balancer
```

**With a custom config path:**

```bash
python -m racedash_balancer --config ~/myconfig.yaml
```

**Override the listen port without editing the file:**

```bash
python -m racedash_balancer --port 20888
```

---

## What you'll see

```
RaceDash Balancer — listening on port 20777
Forwarding to 2 device(s):
  iPad: 192.168.1.100:20777
  iPhone: 192.168.1.101:20777

Press Ctrl+C to stop.

recv   45 pkt/s      12.3 KB/s  |  iPad:   45 pkt/s  0 err  |  iPhone:   45 pkt/s  0 err
```

The stats line updates every second in place. `err` counts packets that failed to send to a specific device — if a device goes offline, its error count rises while the others keep running normally.

Press **Ctrl+C** to stop cleanly.

---

## Troubleshooting

**No packets received (0 pkt/s)**
- Check that F1 25 has UDP telemetry enabled and the IP points to this machine
- Make sure the game is in an active session (main menu does not send telemetry)
- Check your firewall — UDP port 20777 must be open inbound on the machine running this app

**Packets received but errors on a device**
- Confirm the device IP in `config.yaml` is correct
- Make sure RaceDash is open on that device
- Both the app machine and the device must be on the same Wi-Fi network

**Port already in use on startup**
- Another process is using port 20777. Change `listen_port` in `config.yaml` and update the matching setting in F1 25.
