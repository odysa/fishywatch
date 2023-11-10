from datetime import datetime
from typing import Callable, TypeAlias, TypedDict

from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class WebPage:
    soup: BeautifulSoup
    domain: str
    url: str


@dataclass
class ExtractedData:
    price: float
    currency: str
    name: str
    description: str


@dataclass
class ItemData:
    data: ExtractedData
    url: str
    date: datetime


@dataclass
class ParsedResult:
    data: ItemData
    urls: list[str]


ParseFunc: TypeAlias = Callable[[BeautifulSoup], ExtractedData]
