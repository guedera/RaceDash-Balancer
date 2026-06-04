from unittest.mock import MagicMock, patch

from racedash_balancer.config import Destination
from racedash_balancer.forwarder import UDPForwarder
from racedash_balancer.stats import Stats


def _make_forwarder(destinations, stats=None):
    stats = stats or Stats()
    with patch("racedash_balancer.forwarder.socket.socket"):
        fwd = UDPForwarder(destinations, stats)
    return fwd, stats


def test_forward_sends_to_all_destinations():
    dests = [Destination("iPad", "10.0.0.1", 20777), Destination("iPhone", "10.0.0.2", 20777)]
    fwd, stats = _make_forwarder(dests)
    data = b"telemetry"

    fwd.forward(data)

    calls = fwd._sock.sendto.call_args_list
    assert len(calls) == 2
    assert calls[0].args == (data, ("10.0.0.1", 20777))
    assert calls[1].args == (data, ("10.0.0.2", 20777))


def test_forward_records_sent_stats():
    dests = [Destination("iPad", "10.0.0.1", 20777), Destination("iPhone", "10.0.0.2", 20777)]
    fwd, stats = _make_forwarder(dests)

    fwd.forward(b"x")

    assert stats.packets_sent == {"iPad": 1, "iPhone": 1}
    assert stats.errors == {}


def test_forward_records_error_on_os_error():
    dests = [Destination("iPad", "10.0.0.1", 20777), Destination("iPhone", "10.0.0.2", 20777)]
    fwd, stats = _make_forwarder(dests)
    fwd._sock.sendto.side_effect = [OSError("unreachable"), None]

    fwd.forward(b"x")

    assert stats.errors == {"iPad": 1}
    assert stats.packets_sent == {"iPhone": 1}


def test_forward_continues_after_one_destination_fails():
    dests = [Destination("iPad", "10.0.0.1", 20777), Destination("iPhone", "10.0.0.2", 20777)]
    fwd, stats = _make_forwarder(dests)
    fwd._sock.sendto.side_effect = [OSError("unreachable"), None]

    fwd.forward(b"x")

    assert fwd._sock.sendto.call_count == 2
