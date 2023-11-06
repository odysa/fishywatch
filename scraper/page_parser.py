import logging
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from infra.channel import Receiver, Sender
from infra.exception import ParseFuncNotFound
from infra.types import PageMsg, PageResult, ParsedData, ParseFunc
from utils import filter_urls


class Parser(ABC):
    @abstractmethod
    def parse(self, page_msg: PageMsg) -> PageResult | None:
        ...


def get_urls(soup: BeautifulSoup) -> list[str]:
    links = soup.find_all("a")
    return [link.get("href") for link in links]


class FishyParser(Parser):
    parser_func_map: dict[str, ParseFunc]

    def __init__(self, parser_func_map: dict[str, ParseFunc]) -> None:
        self.parser_func_map = parser_func_map

    def parse(self, page_msg: PageMsg) -> PageResult:
        soup = page_msg["soup"]
        domain = page_msg["domain"]

        if domain not in self.parser_func_map:
            raise ParseFuncNotFound(f"{domain} does not have a parse function")

        func: ParseFunc = self.parser_func_map[domain]
        parsed_result: ParsedData = func(soup)

        urls = filter_urls(domain, get_urls(soup))
        return {"data": parsed_result, "urls": urls}


async def parser_worker(
        parser: Parser,
        page_rx: Receiver[PageMsg],
        data_tx: Sender[PageResult],
):
    while page_msg := await page_rx.recv():
        try:
            res: PageResult = parser.parse(page_msg)
            data = res["data"]
            urls = res["urls"]

            msg = PageResult(data=data, urls=urls)
            await data_tx.send(msg)
        except Exception as e:
            logging.error(str(e))
