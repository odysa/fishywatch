from asyncpg.connection import Connection as PgConnection
from tortoise import Tortoise

from infra.exception import Unreachable
from infra.model import Item
from infra.types import ItemData
from scraper.saver import Saver


class PostgresSaver(Saver):
    conn: PgConnection

    def __init__(self, conn: PgConnection):
        self.conn = conn

    async def save(self, item_data: ItemData):
        if item_data.extracted is None:
            raise Unreachable('data to save impossible to be None')

        # insert into items
        if not self.data_exists(item_data):
            data = item_data.extracted
            if data is None:
                pass
            item = Item()
            item.name = data.name
            item.description = data.description
            item.url = item_data.url
            await item.save()

    async def close(self):
        await Tortoise.close_connections()

    @staticmethod
    async def data_exists(item_data: ItemData) -> bool:
        return await Item.exists(name=item_data.extracted.name, url=item_data.url)
