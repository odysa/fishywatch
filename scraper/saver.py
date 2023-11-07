from abc import ABC

import aiofiles

from infra.channel import Receiver
from infra.types import ItemData


class Saver(ABC):
    async def save(self, data: ItemData):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError


class CSVSaver(Saver):
    _file_name: str

    def __init__(self, file_name: str):
        self._file_name = file_name
        self._f = None

    async def save(self, data: ItemData):
        if not self._f:
            self._f = await aiofiles.open(self._file_name, "w+")
            keys = data.keys()
            await self._f.write(",".join(keys))
            await self._f.write("\n")

        await self._f.write(",".join([str(v).encode('unicode_escape').decode() for v in data.values()]))
        await self._f.write("\n")

    async def close(self):
        await self._f.close()


async def saver_worker(saver: Saver, data_rx: Receiver[ItemData]):
    while data_to_save := await data_rx.recv():
        await saver.save(data_to_save)

    await saver.close()
