from typing import Callable, TypedDict

from bs4 import BeautifulSoup


class PageMsg(TypedDict):
    soup: BeautifulSoup
    domain: str


class ParsedResult(TypedDict):
    price: float
    currency: str
    name: str
    description: str


class PageRes(TypedDict):
    urls: list[str]
    data: ParsedResult


type ParseFunc = Callable[[BeautifulSoup], ParsedResult]
