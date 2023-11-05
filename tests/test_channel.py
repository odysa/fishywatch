import asyncio
import random

import pytest

from infra.channel import Receiver, Sender, channel


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "msg", ["hello", "!%$#@%#$%$#", "1232143", 123123, [1231241231]]
)
async def test_channel(msg: int | str | list):
    tx, rx = channel()
    await tx.send(msg)

    assert await rx.recv() == msg


@pytest.mark.asyncio
@pytest.mark.parametrize("n", [10, 100, 1000, 10000, 100000])
async def test_concurrent_channel(n: int):
    data = [random.randint(0, n) for _ in range(n)]

    async def receiver(rx: Receiver):
        for i in range(n):
            assert await rx.recv() == data[i]

    async def sender(tx: Sender):
        for i in range(n):
            await tx.send(data[i])

    t_tx, t_rx = channel()
    rx_handle = asyncio.create_task(receiver(t_rx))
    tx_handle = asyncio.create_task(sender(t_tx))
    await rx_handle
    await tx_handle
