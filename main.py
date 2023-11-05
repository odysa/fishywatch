import asyncio as tokio

from fetcher import RequestsFetcher, fetcher_worker
from infra.channel import channel
from page_parser import FishyParser, parser_worker


async def start_fetcher_and_parser():
    url_tx, url_rx = channel()
    page_tx, page_rx = channel()
    parsed_res_tx, parsed_res_rx = channel()

    fetcher_task = tokio.create_task(
        fetcher_worker(
            RequestsFetcher(),
            url_rx,
            page_tx,
        )
    )

    parser_task = tokio.create_task(
        parser_worker(
            FishyParser(dict()),
            page_rx,
            parsed_res_tx
        )
    )

    return fetcher_task, parser_task, url_tx, parsed_res_rx


async def main():
    # urls = ["https://www.baidu.com"]
    fetcher_tasks = []
    parser_tasks = []
    url_txs = []

    for _ in range(10):
        fetcher_task, parser_task, url_tx, parsed_res_rx = start_fetcher_and_parser()
        url_txs.append(url_tx)
        fetcher_tasks.append(fetcher_task)
        parser_tasks.append(parser_task)

    for t in fetcher_tasks:
        await t
    for t in parser_tasks:
        await t


if __name__ == "__main__":
    tokio.run(main())
