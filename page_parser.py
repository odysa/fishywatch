from abc import ABC, abstractmethod

from infra.channel import Receiver, Sender
from infra.exception import ParseFuncNotFound
from infra.types import PageMsg, PageRes, ParseFunc, ParsedResult
from bs4 import BeautifulSoup
import logging


class Parser(ABC):
    @abstractmethod
    def parse(self, page_msg: PageMsg) -> PageRes | None:
        ...


def get_urls(soup: BeautifulSoup) -> list[str]:
    links = soup.find_all("a")
    return [link.get("href") for link in links]


class FishyParse(Parser):
    parser_func_map: dict[str, ParseFunc]

    def __init__(self, parser_func_map: dict[str, ParseFunc]) -> None:
        self.parser_func_map = parser_func_map

    def parse(self, page_msg: PageMsg) -> PageRes:
        soup = page_msg["soup"]
        domain = page_msg["domain"]

        if domain not in self.parser_func_map:
            raise ParseFuncNotFound(f"{domain} does not have a parse function")

        func: ParseFunc = self.parser_func_map[domain]
        parsed_result: ParsedResult = func(soup)

        urls = get_urls(soup)
        return {"data": parsed_result, "urls": urls}


async def parser_worker(
    parser: Parser,
    page_rx: Receiver[PageMsg],
    data_tx: Sender[ParsedResult],
    url_tx: Sender[str],
):
    while page_msg := await page_rx.recv():
        try:
            res: PageRes = parser.parse(page_msg)
            data = res["data"]
            urls = res["urls"]

            await data_tx.send(data)
            for url in urls:
                await url_tx.send(url)

        except ParseFuncNotFound as e:
            logging.exception(str(e))
