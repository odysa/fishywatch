"""
Module: web_fetcher

This module provides classes and functions for fetching web pages,
parsing them, and sending the parsed content for processing.

Classes:
- Fetcher (abstract base class): Represents a web page fetcher with an abstract `fetch` method.
- RequestsFetcher: Implements the `Fetcher` interface using aiohttp for web page fetching.

Functions:
- fetcher_worker: An asynchronous worker function that fetches web pages,
parses them with BeautifulSoup, and sends them for processing.
"""
import asyncio
import logging
from abc import ABC, abstractmethod

import aiohttp
import tldextract
from bs4 import BeautifulSoup

from infra.channel import Receiver, Sender
from infra.types import WebPage


class Fetcher(ABC):
    @abstractmethod
    async def fetch(self, url: str) -> str:
        """
        Abstract base class for web page fetchers.

        Args:
            url (str): The URL of the web page to fetch.

        Returns:
            str: The content of the fetched web page as a string.
        """
        raise NotImplementedError


class RequestsFetcher(Fetcher):
    limit: int
    timeout: int

    def __init__(self, limit: int = 1, timeout: int = 4) -> None:
        """
        Initialize the RequestsFetcher.

        Args:
            limit (int): The maximum number of concurrent requests.
            timeout (int): The timeout value for web requests in seconds.
        """
        self.limit = limit
        self.timeout = timeout

    async def fetch(self, url: str) -> str:
        """
        Fetch a web page using aiohttp.

        Args:
            url (str): The URL of the web page to fetch.

        Returns:
            str: The content of the fetched web page as a string.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.text()


async def fetcher_worker(
        fetcher: Fetcher,
        url_rx: Receiver[str],
        page_tx: Sender[WebPage]
) -> None:
    """
    Asynchronous worker function that fetches web pages, parses them with BeautifulSoup, and sends them for processing.

    Args:
        fetcher (Fetcher): The web page fetcher implementing the `Fetcher` abstract class.
        url_rx (Receiver[str]): A receiver for receiving URLs to fetch.
        page_tx (Sender[WebPage]): A sender for sending parsed web pages as `WebPage` objects.

    Returns:
        None

    This function processes URLs from the `url_rx` channel by fetching the web page content using the provided fetcher,
    parsing it with BeautifulSoup using the 'lxml' parser, and extracting the domain from the URL using 'tldextract'.
    The parsed web page content, domain, and URL are packaged into a `WebPage` object and sent to the `page_tx` channel.
    If an exception occurs during the process, it is logged as an error.

    Note:
    - The function sleeps for 0.5 seconds after processing each URL to avoid overloading the server.

    Example Usage:
    ```python
    url_receiver = create_url_receiver()
    page_sender = create_page_sender()
    fetcher = RequestsFetcher(limit=5, timeout=10)

    asyncio.create_task(fetcher_worker(fetcher, url_receiver, page_sender))
    ```
    """
    while url := await url_rx.recv():
        try:
            page = await fetcher.fetch(url)
            soup = BeautifulSoup(page, "lxml")
            domain = tldextract.extract(url).domain
            msg = WebPage(domain=domain, soup=soup, url=url)
            await page_tx.send(msg)
            await asyncio.sleep(0.5)
        except Exception as e:
            logging.error(str(e))
