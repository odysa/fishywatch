import logging
from abc import ABC, abstractmethod
from datetime import datetime

from bs4 import BeautifulSoup

from infra.channel import Receiver, Sender
from infra.exception import ParseFuncNotFound
from infra.types import ExtractedData, ItemData, ParsedResult, ParseFunc, WebPage

from .utils import filter_urls


class Parser(ABC):
    @abstractmethod
    def parse(self, page_msg: WebPage) -> ParsedResult | None:
        raise NotImplementedError


def get_urls(soup: BeautifulSoup) -> list[str]:
    links = soup.find_all("a")
    return [link.get("href") for link in links]


class FishyParser(Parser):
    parser_func_map: dict[str, ParseFunc]

    def __init__(self, parser_func_map: dict[str, ParseFunc]) -> None:
        self.parser_func_map = parser_func_map

    def parse(self, page_msg: WebPage) -> ParsedResult:
        soup = page_msg.soup
        domain = page_msg.domain

        if domain not in self.parser_func_map:
            raise ParseFuncNotFound(f"{domain} does not have a parse function")

        func: ParseFunc = self.parser_func_map[domain]
        parsed_data: ExtractedData = func(soup)
        item_data = ItemData(extracted=parsed_data, url=page_msg.url, date=datetime.now())
        urls = filter_urls(domain, get_urls(soup))
        return ParsedResult(data=item_data, urls=urls)


async def parser_worker(
        parser: Parser,
        page_rx: Receiver[WebPage],
        data_tx: Sender[ParsedResult],
):
    while page_msg := await page_rx.recv():
        try:
            res: ParsedResult = parser.parse(page_msg)
            data = res.data
            urls = res.urls

            msg = ParsedResult(data=data, urls=urls)
            await data_tx.send(msg)
        except Exception as e:
            logging.error(str(e))
