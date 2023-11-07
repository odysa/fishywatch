from typing import Callable, TypeAlias, TypedDict

from bs4 import BeautifulSoup


class WebPage(TypedDict):
    soup: BeautifulSoup
    domain: str
    url: str


class ParsedData(TypedDict):
    price: float
    currency: str
    name: str
    description: str


class ItemData(TypedDict):
    parsed_data: ParsedData
    url: str


class ParsedResult(TypedDict):
    data: ItemData
    urls: list[str]


ParseFunc: TypeAlias = Callable[[BeautifulSoup], ParsedData]
