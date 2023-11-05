from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from infra.channel import Receiver, Sender
from infra.types import PageMsg
import requests


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

    def fetch(self, url: str) -> bytes:
        resp = requests.get(url, timeout=self.timeout)
        return resp.content


async def fetcher_worker(
        fetcher: Fetcher, url_rx: Receiver[str], soup_tx: Sender[PageMsg]
) -> None:
    """
    Args:
        fetcher: web page fetcher
        url_rx: url receiver
        soup_tx: parsed beautifulsoup sender

    Returns: None
    """
    while url := await url_rx.recv():
        page = fetcher.fetch(url)
        _soup = BeautifulSoup(page.content)
