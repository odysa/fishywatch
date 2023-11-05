import asyncio as tokio

from fetcher import RequestsFetcher, fetcher_worker
from infra.channel import channel
from page_parser import FishyParser, parser_worker


async def main():
    urls = []

    url_tx, url_rx = channel()
    page_tx, page_rx = channel()
    parsed_res_tx, parsed_res_rx = channel()
    parsed_url_tx, parsed_url_rx = channel()

    fetcher_task = tokio.create_task(
        fetcher_worker(
            RequestsFetcher(),
            url_rx,
            page_tx,
        )
    )

    parser_task = tokio.create_task(
        parser_worker(FishyParser(dict()), page_rx, parsed_res_tx, parsed_url_tx)
    )

    for url in urls:
        await url_tx.send(url)

    while url := await parsed_url_rx.recv():
        await url_tx.send(url)

    await fetcher_task
    await parser_task


if __name__ == "__main__":
    tokio.run(main())
