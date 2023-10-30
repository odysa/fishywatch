from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
from traitlets import Callable

from infra.channel import Receiver
from infra.types import PageMsg, PageRes, ParseFunc


class Parser(ABC):
    @abstractmethod
    def parse(self, page_msg: PageMsg) -> PageRes | None:
        pass


class FishyParse(Parser):
    parser_func_map: dict[str, ParseFunc]

    def __init__(self, parser_func_map: dict[str, ParseFunc]) -> None:
        self.parser_func_map = parser_func_map

    def parse(self, page_msg: PageMsg) -> PageRes:
        soup = page_msg["soup"]
        domain = page_msg["domain"]
        func = self.parser_func_map[domain]
        if not func:
            return None
        soup.find_all("a")
        return {"data": [], "urls": []}


PARSER_FUNC_MAP: dict[str, Callable[[BeautifulSoup]]] = {"petre": None}


async def parser_worker(parser: Parser, page_rx: Receiver[PageMsg]):
    while page_msg := await page_rx.recv():
        res = parser.parse(page_msg)
