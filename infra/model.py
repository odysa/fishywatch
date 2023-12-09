from tortoise import fields
from tortoise.models import Model


class Item(Model):
    id = fields.IntField(pk=True)
    name = fields.TextField()
    description = fields.TextField()
    url = fields.TextField()
    updated_at = fields.DatetimeField(auto_now=True)


# Version of item. ie 14000 of Stella
class ItemVersion(Model):
    id = fields.IntField(pk=True)
    item = fields.ForeignKeyField("model.Item", related_name="item")
    version = fields.TextField()


class PriceHistory(Model):
    id = fields.IntField(pk=True)
    version = fields.ForeignKeyField("model.ItemVersion", related_name="version")
    item = fields.ForeignKeyField("model.Item", related_name="item")
    price = fields.FloatField()
    currency = fields.TextField()
    date = fields.DatetimeField()
    updated_at = fields.DatetimeField(auto_now=True)


class EmailNotification(Model):
    id = fields.IntField(pk=True)
    item = fields.ForeignKeyField("model.Item", related_name="item")
    email = fields.TextField()


class ClickCount(Model):
    id = fields.IntField(pk=True)
    item = fields.ForeignKeyField("model.Item", related_name="item")
    click_count = fields.IntField(default=0)
