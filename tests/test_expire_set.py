import time
from datetime import timedelta

import pytest

from infra.expire_set import ExpireSet


def test_expire_set_limit():
    s = ExpireSet[int](limit=1, expire_time=timedelta(seconds=0.5))
    s.add(1)
    time.sleep(0.5)
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


@pytest.mark.parametrize("n", [100, 1000, 10000, 100000, 1000000])
def test_expire_set_not_expired(n):
    s = ExpireSet[int](limit=n + 1, expire_time=timedelta(days=100))
    for i in range(n):
        s.add(i)

    assert len(s) == n

    for i in range(n):
        assert i in s


@pytest.mark.parametrize("n", [100, 1000, 10000, 100000, 1000000])
def test_expire_set_values(n):
    s = ExpireSet[int](limit=n + 1, expire_time=timedelta(days=100))
    for i in range(n):
        s.add(i)

    assert len(s) == n

    values = set(s.values())
    assert len(values) == n
    for i in range(n):
        assert i in values
