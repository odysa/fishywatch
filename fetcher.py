from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup

from infra.channel import Receiver, Sender
from infra.types import PageMsg


class Fetcher(ABC):
    @abstractmethod
    def fetch(self, url: str) -> BeautifulSoup:
        pass


class RequestsFetcher(Fetcher):
    limit: int
    timeout: int

    def __init__(self, limit: int = 1, timeout: int = 5) -> None:
        self.limit = limit
        self.timeout = timeout

    def fetch(self, url: str) -> BeautifulSoup:
        resp = requests.get(url, timeout=self.timeout)
        return resp.content


async def fetcher_worker(
    fetcher: Fetcher, url_rx: Receiver[str], soup_tx: Sender[PageMsg]
) -> None:
    while url := await url_rx.recv():
        page = fetcher.fetch(url)
        soup = BeautifulSoup(page.content)
        await soup_tx.send({"soup": soup, "parse_func": None})
