from typing import Generic, TypeAlias, TypedDict, TypeVar

from bs4 import BeautifulSoup
from traitlets import Callable

_T = TypeVar("_T")


class PageRes(TypedDict, Generic[_T]):
    urls: list[str]
    data: _T


class PageMsg(TypedDict):
    soup: BeautifulSoup
    domain: str


ParseFunc: TypeAlias = Callable[[BeautifulSoup]]
