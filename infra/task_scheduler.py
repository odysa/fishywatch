import asyncio
from typing import Generic, TypeVar

from channel import Receiver, Sender, channel

_T = TypeVar("_T")
_U = TypeVar("_U")


class TaskScheduler(Generic[_T, _U]):
    _txs = list[asyncio.Task[_T]]
    _rx: Receiver[_U]
    _free_tasks: list[_txs]

    def __init__(self, txs: list[Sender[_T]], rx: Receiver[_U]):
        self._txs = txs
        self._rx = rx

    @classmethod
    def new(cls, txs: list[Sender[_T]]) -> Sender[_U]:
        tx, rx = channel()
        cls(txs, rx)
        return tx

    async def run(self):
        pass
