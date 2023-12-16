import os

from tortoise import Tortoise

from scraper.utils import to_int

DEFAULT_FETCHER_COUNT = 5
DEFAULT_PARSER_COUNT = 5
DEFAULT_SAVER_COUNT = 5


class Config:
    db_url: str
    fetcher_count: int
    parser_count: int
    saver_count: int

    def __init__(self):
        self.fetcher_count = to_int(os.environ.get('fetcher_count'), DEFAULT_FETCHER_COUNT)
        self.parser_count = to_int(os.environ.get('parser_count'), DEFAULT_PARSER_COUNT)
        self.saver_count = to_int(os.environ.get('saver_count'), DEFAULT_SAVER_COUNT)
        self.db_url = os.environ.get('db_url')


async def init_db(config: Config):
    await Tortoise.init(
        db_url=config.db_url,
        modules={"models": ['infra.model']}

    )
    await Tortoise.generate_schemas()
