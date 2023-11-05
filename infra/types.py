from typing import Generic, TypeAlias, TypedDict, TypeVar

from bs4 import BeautifulSoup
from typing import Callable


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
