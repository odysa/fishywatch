from dataclasses import dataclass
from datetime import datetime
from typing import Callable, TypeAlias

from bs4 import BeautifulSoup


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
    version: str


@dataclass
class ItemData:
    extracted: ExtractedData
    url: str
    date: datetime

    @staticmethod
    def keys():
        return ["name", "currency", "price", "date", "url", "date"]

    def values(self):
        return [
            self.extracted.name,
            self.extracted.currency,
            self.extracted.price,
            self.extracted.description,
            self.url,
            self.date,
        ]


@dataclass
class ParsedResult:
    data: ItemData
    urls: list[str]


ParseFunc: TypeAlias = Callable[[BeautifulSoup], ExtractedData]
