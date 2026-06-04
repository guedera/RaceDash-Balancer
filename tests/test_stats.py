from racedash_balancer.stats import Stats, _format_bytes


def test_record_recv_accumulates():
    s = Stats()
    s.record_recv(100)
    s.record_recv(200)
    assert s.packets_recv == 2
    assert s.bytes_recv == 300


def test_record_sent_accumulates():
    s = Stats()
    s.record_sent("iPad")
    s.record_sent("iPad")
    s.record_sent("iPhone")
    assert s.packets_sent == {"iPad": 2, "iPhone": 1}


def test_record_error_accumulates():
    s = Stats()
    s.record_error("iPad")
    s.record_error("iPad")
    assert s.errors == {"iPad": 2}


def test_snapshot_is_independent_copy():
    s = Stats()
    s.record_recv(50)
    snap = s.snapshot()
    s.record_recv(50)
    assert snap.packets_recv == 1
    assert snap.bytes_recv == 50
    assert s.packets_recv == 2


def test_snapshot_dicts_are_copies():
    s = Stats()
    s.record_sent("iPad")
    snap = s.snapshot()
    s.record_sent("iPad")
    assert snap.packets_sent == {"iPad": 1}


def test_format_bytes_units():
    assert _format_bytes(500) == "500 B/s"
    assert _format_bytes(2048) == "2.0 KB/s"
    assert _format_bytes(2 * 1024 * 1024) == "2.0 MB/s"
