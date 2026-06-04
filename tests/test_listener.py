import threading
from unittest.mock import MagicMock, patch

from racedash_balancer.listener import UDPListener
from racedash_balancer.stats import Stats


def _start_listener(listener):
    t = threading.Thread(target=listener.start, daemon=True)
    t.start()
    return t


def _make_mock_socket(packets):
    """Returns a mock socket that yields packets then raises OSError to stop the loop."""
    mock_sock = MagicMock()
    responses = [(pkt, ("127.0.0.1", 20777)) for pkt in packets]
    responses.append(OSError("stop"))
    mock_sock.recvfrom.side_effect = responses
    return mock_sock


def test_recv_loop_calls_on_packet():
    received = []
    stats = Stats()
    listener = UDPListener(port=20777, on_packet=received.append, stats=stats)

    mock_sock = _make_mock_socket([b"pkt1", b"pkt2"])

    with patch("racedash_balancer.listener.socket.socket", return_value=mock_sock):
        with patch("racedash_balancer.listener.time.sleep"):
            listener._running = True
            listener._bind()
            try:
                listener._recv_loop()
            except OSError:
                pass

    assert received == [b"pkt1", b"pkt2"]


def test_recv_loop_records_stats():
    stats = Stats()
    listener = UDPListener(port=20777, on_packet=lambda _: None, stats=stats)
    mock_sock = _make_mock_socket([b"hello", b"world!"])

    with patch("racedash_balancer.listener.socket.socket", return_value=mock_sock):
        with patch("racedash_balancer.listener.time.sleep"):
            listener._running = True
            listener._bind()
            try:
                listener._recv_loop()
            except OSError:
                pass

    assert stats.packets_recv == 2
    assert stats.bytes_recv == len(b"hello") + len(b"world!")


def test_close_stops_running():
    stats = Stats()
    listener = UDPListener(port=20777, on_packet=lambda _: None, stats=stats)

    mock_sock = MagicMock()
    mock_sock.recvfrom.side_effect = lambda _: (_ for _ in ()).throw(OSError("closed"))

    with patch("racedash_balancer.listener.socket.socket", return_value=mock_sock):
        with patch("racedash_balancer.listener.time.sleep"):
            t = _start_listener(listener)
            listener.close()
            t.join(timeout=2)

    assert not listener._running
    assert not t.is_alive()


def test_socket_error_triggers_retry():
    stats = Stats()
    calls = []
    listener = UDPListener(port=20777, on_packet=lambda _: None, stats=stats)

    bind_count = 0

    original_bind = listener._bind

    def counting_bind():
        nonlocal bind_count
        bind_count += 1
        if bind_count >= 2:
            listener._running = False
        raise OSError("bind failed")

    listener._bind = counting_bind

    with patch("racedash_balancer.listener.time.sleep"):
        listener.start()

    assert bind_count >= 2
