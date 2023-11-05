from typing import Callable, TypedDict

from bs4 import BeautifulSoup


class PageMsg(TypedDict):
    soup: BeautifulSoup
    domain: str


class ParsedData(TypedDict):
    price: float
    currency: str
    name: str
    description: str


class PageResult(TypedDict):
    urls: list[str]
    data: ParsedData


type ParseFunc = Callable[[BeautifulSoup], ParsedData]
