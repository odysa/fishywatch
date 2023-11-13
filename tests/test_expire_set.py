import time
from datetime import timedelta

from infra.expire_set import ExpireSet


def test_expire_set_limit():
    s = ExpireSet[int](limit=1, expire_time=timedelta(minutes=1))
    s.add(1)
    s.add(2)
    assert 1 not in s


def test_expire_set_expire_time():
    s = ExpireSet[int](limit=100, expire_time=timedelta(milliseconds=1))
    s.add(1)
    s.add(2)
    s.add(3)
    time.sleep(0.1)
    s.evict_expire()
    assert 1 not in s
    assert 2 not in s
    assert 3 not in s
    assert len(s) == 0
