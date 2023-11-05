import asyncio as tokio

from fetcher import RequestsFetcher, fetcher_worker
from infra.channel import Receiver, Sender, channel
from infra.types import PageMsg, PageResult
from page_parser import FishyParser, parser_worker
from parserfuncs import parse_peche


def start_fetcher_and_parser(
        tg: tokio.TaskGroup,
        url_rx: Receiver[str],
        page_tx: Sender[PageMsg],
        page_rx: Receiver[PageMsg],
        parsed_res_tx: Sender[PageResult]
):
    fetcher_task = tg.create_task(
        fetcher_worker(
            RequestsFetcher(),
            url_rx,
            page_tx,
        )
    )

    parser_task = tg.create_task(
        parser_worker(
            FishyParser({"pechextreme": parse_peche}),
            page_rx,
            parsed_res_tx
        )
    )

    return fetcher_task, parser_task


async def main():
    visited = set()
    urls = ["https://www.pechextreme.com/en"]

    url_tx, url_rx = channel()
    page_tx, page_rx = channel()
    parsed_res_tx, parsed_res_rx = channel()

    async with tokio.TaskGroup() as tg:
        for _ in range(100):
            start_fetcher_and_parser(
                tg,
                url_rx,
                page_tx,
                page_rx,
                parsed_res_tx
            )

        for url in urls:
            visited.add(url)
            await url_tx.send(url)

        while parsed_res := await parsed_res_rx.recv():
            res: PageResult = parsed_res
            for url in res.get("urls"):
                if url not in visited:
                    await url_tx.send(url)
                    visited.add(url)
            if res["data"]:
                print(res["data"])


if __name__ == "__main__":
    tokio.run(main())
