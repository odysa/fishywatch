import os

from tortoise import Tortoise


async def init_db():
    await Tortoise.init(
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ['infra.model']}
    )

    await Tortoise.generate_schemas()
