from tortoise import fields
from tortoise.models import Model


class Item(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    description = fields.TextField()
    updated_at = fields.DatetimeField(auto_now=True)


class PriceHistory(Model):
    id = fields.IntField(pk=True)
    item = fields.ForeignKeyField("models.Item", related_name="item")
    price = fields.FloatField()
    currency = fields.TextField()
    date = fields.DatetimeField()
    updated_at = fields.DatetimeField(auto_now=True)
