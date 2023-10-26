import asyncio
from asyncio import Queue
from typing import Generic, TypeVar

import requests

_T = TypeVar("_T")


class Channel(Generic[_T]):
    q: Queue

    def __init__(self) -> None:
        self.q = Queue()

    async def send(self, item: _T) -> None:
        self.q.put(item)

    async def recv(self) -> _T:
        self.q.get()


async def fetch(url_chan: Channel[str], page_chan: Channel[str]):
    while url := await url_chan.recv():
        _page = requests.get(url)
        await page_chan.send("get " + url)


async def parse(rx_chan: Channel[str]):
    while item := await rx_chan.send():
        print(item)


async def main():
    url_chan = Channel[str]()
    page_chan = Channel[str]()
    n = 100
    for _ in range(n):
        tasks = asyncio.gather(fetch(url_chan, page_chan), parse(page_chan))
    await url_chan.send("google")
    await url_chan.send("linux")
    await tasks


asyncio.run(main())
