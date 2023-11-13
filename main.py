import asyncio as tokio

from dotenv import load_dotenv

from infra.channel import channel
from infra.types import ParsedResult
from scraper.fetcher import RequestsFetcher, fetcher_worker
from scraper.page_parser import FishyParser, parser_worker
from scraper.parserfuncs import parse_peche
from scraper.saver import CSVSaver, saver_worker
from scraper.config import Config, init_db

PARSER_FUNCS = {
    "pechextreme": parse_peche
}


async def main():
    load_dotenv()

    config = Config()
    await init_db(config)

    visited = set()
    urls = ["https://www.pechextreme.com/en"]

    url_tx, url_rx = channel()
    page_tx, page_rx = channel()
    parsed_res_tx, parsed_res_rx = channel()

    parsed_data_tx, parsed_data_rx = channel()

    async with tokio.TaskGroup() as tg:
        for _ in range(config.fetcher_count):
            tg.create_task(
                fetcher_worker(
                    RequestsFetcher(),
                    url_rx,
                    page_tx,
                )
            )

        for _ in range(config.parser_count):
            tg.create_task(
                parser_worker(
                    FishyParser(PARSER_FUNCS),
                    page_rx,
                    parsed_res_tx
                )
            )

        tg.create_task(
            saver_worker(CSVSaver("data.csv"), parsed_data_rx)
        )

        for url in urls:
            visited.add(url)
            await url_tx.send(url)

        while parsed_res := await parsed_res_rx.recv():
            res: ParsedResult = parsed_res
            for url in res.urls:
                if url not in visited:
                    await url_tx.send(url)
                    visited.add(url)

            if res.data and res.data.extracted:
                await parsed_data_tx.send(res.data)


if __name__ == "__main__":
    tokio.run(main())
