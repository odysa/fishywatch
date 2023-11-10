from infra.types import ItemData, ExtractedData
from infra.exception import Unreachable
from scraper.saver import Saver
from asyncpg.connection import Connection as PgConnection


class PostgresSaver(Saver):
    conn: PgConnection

    def __init__(self, conn: PgConnection):
        self.conn = conn

    async def save(self, item_data: ItemData):
        data = item_data.data
        if data is None:
            raise Unreachable('data to save impossible to be None')
        pass

    async def close(self):
        pass

    async def data_exists(self, data: ExtractedData) -> bool:
        await self.conn.close()
        self.conn.fetch()
        return True
