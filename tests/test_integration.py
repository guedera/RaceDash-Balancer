"""
Integration test: simulates F1 25 sending UDP packets and verifies they
arrive at destination sockets on the loopback interface.
"""
import socket
import threading
import time

from racedash_balancer.config import Destination
from racedash_balancer.forwarder import UDPForwarder
from racedash_balancer.listener import UDPListener
from racedash_balancer.stats import Stats

_LISTEN_PORT = 34100
_DEST_PORT_1 = 34101
_DEST_PORT_2 = 34102
_PACKETS = [b"F1_PKT_%d" % i for i in range(5)]


def _open_receiver(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(2.0)
    sock.bind(("127.0.0.1", port))
    return sock


def test_packets_relayed_to_all_destinations():
    recv1 = _open_receiver(_DEST_PORT_1)
    recv2 = _open_receiver(_DEST_PORT_2)

    stats = Stats()
    dests = [
        Destination("dev1", "127.0.0.1", _DEST_PORT_1),
        Destination("dev2", "127.0.0.1", _DEST_PORT_2),
    ]
    forwarder = UDPForwarder(dests, stats)
    listener = UDPListener(port=_LISTEN_PORT, on_packet=forwarder.forward, stats=stats)

    t = threading.Thread(target=listener.start, daemon=True)
    t.start()
    time.sleep(0.05)

    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for pkt in _PACKETS:
        sender.sendto(pkt, ("127.0.0.1", _LISTEN_PORT))
    sender.close()

    time.sleep(0.05)
    listener.close()
    forwarder.close()

    received1 = []
    received2 = []
    try:
        while True:
            received1.append(recv1.recv(65535))
    except (socket.timeout, OSError):
        pass
    try:
        while True:
            received2.append(recv2.recv(65535))
    except (socket.timeout, OSError):
        pass

    recv1.close()
    recv2.close()

    assert received1 == _PACKETS
    assert received2 == _PACKETS
    assert stats.packets_recv == len(_PACKETS)
    assert stats.packets_sent == {"dev1": len(_PACKETS), "dev2": len(_PACKETS)}
