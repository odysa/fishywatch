from bs4 import BeautifulSoup

from infra.types import ParsedData


def parse_peche(soup: BeautifulSoup) -> ParsedData | None:
    name_tag = soup.find("h1", {"class": "product_name", "itemprop": "name"})
    name = None if not name_tag else name_tag.text

    price_tag = soup.find("span", {"class": "price", "itemprop": "price"})
    price = None if not price_tag else price_tag.attrs.get("content")

    currency_tag = soup.find("meta", {"itemprop": "priceCurrency"})
    currency = None if not currency_tag else currency_tag.attrs.get("content")

    description_tag = soup.find("div", {"class": "product_desc", "itemprop": "description"})
    description = None if not description_tag else description_tag.find("p").text

    if not price:
        return None

    return ParsedData(
        price=float(price),
        currency=currency,
        name=name,
        description=description
    )
