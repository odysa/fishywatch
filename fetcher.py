import logging
from abc import ABC, abstractmethod

import requests
import tldextract
from bs4 import BeautifulSoup

from infra.channel import Receiver, Sender
from infra.types import PageMsg


class Fetcher(ABC):
    @abstractmethod
    def fetch(self, url: str) -> bytes:
        ...


class RequestsFetcher(Fetcher):
    limit: int
    timeout: int

    def __init__(self, limit: int = 1, timeout: int = 4) -> None:
        self.limit = limit
        self.timeout = timeout

    def fetch(self, url: str) -> bytes:
        resp = requests.get(url, timeout=self.timeout)
        return resp.content


async def fetcher_worker(
        fetcher: Fetcher, url_rx: Receiver[str], page_tx: Sender[PageMsg]
) -> None:
    """
    Args:
        fetcher: web page fetcher
        url_rx: url receiver
        page_tx: parsed beautifulsoup sender

    Returns: None
    """
    while url := await url_rx.recv():
        try:
            page = fetcher.fetch(url)
            soup = BeautifulSoup(page, "lxml")
            domain = tldextract.extract(url).domain
            msg = PageMsg(domain=domain, soup=soup)
            await page_tx.send(msg)
        except Exception as e:
            logging.error(str(e))
