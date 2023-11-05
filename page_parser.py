from abc import ABC, abstractmethod

from infra.channel import Receiver
from infra.exception import ParseFuncNotFound
from infra.types import PageMsg, PageRes, ParseFunc
from bs4 import BeautifulSoup


class Parser(ABC):
    @abstractmethod
    def parse(self, page_msg: PageMsg) -> PageRes | None:
        pass


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
        func = self.parser_func_map[domain]

        if not func:
            raise ParseFuncNotFound

        urls = get_urls(soup)
        return {"data": [], "urls": urls}


async def parser_worker(parser: Parser, page_rx: Receiver[PageMsg]):
    while page_msg := await page_rx.recv():
        try:
            res: PageRes = parser.parse(page_msg)
            _urls = res.get("urls")
        except ParseFuncNotFound:
            pass
