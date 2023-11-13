import logging

from tortoise import Tortoise
from tortoise.exceptions import DoesNotExist, MultipleObjectsReturned
from tortoise.queryset import QuerySet

from infra.exception import PriceHistoryNotFound, Unreachable
from infra.model import Item, PriceHistory
from infra.types import ItemData
from scraper.saver import Saver


class PostgresSaver(Saver):

    def __init__(self):
        ...

    async def save(self, item_data: ItemData):
        if item_data is None or item_data.extracted is None:
            raise Unreachable('data to save impossible to be None')

        try:
            item = await Item.get(name=item_data.extracted.name, url=item_data.url)
            await self.add_price_history(item_data, item)
        except DoesNotExist:
            await self.save_item_data(item_data)
        except MultipleObjectsReturned:
            logging.error("Impossible to have multiple objects")

    async def close(self):
        await Tortoise.close_connections()

    @staticmethod
    async def data_exists(item_data: ItemData) -> bool:
        return await Item.exists(name=item_data.extracted.name, url=item_data.url)

    @staticmethod
    async def save_item_data(item_data: ItemData):
        data = item_data.extracted

        if data is None:
            pass

        item = Item()
        item.name = data.name
        item.description = data.description
        item.url = item_data.url

        await item.save()

    @staticmethod
    async def get_latest_price_history(item: Item) -> float:
        price_history: PriceHistory = await QuerySet(PriceHistory).filter(item=item).order_by("-updated_at").first()

        if price_history is None:
            raise PriceHistoryNotFound("No price history")
        return price_history.price

    @staticmethod
    async def add_price_history(item_data: ItemData, item: Item):
        latest_price = PostgresSaver.get_latest_price_history(item)

        # price no change
        if latest_price == item_data.extracted.price:
            return

        history = PriceHistory()
        history.price = item_data.extracted.price
        history.date = item_data.date
        history.currency = item_data.extracted.currency
        history.item = item
        await history.save()
