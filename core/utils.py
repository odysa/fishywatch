import re
from urllib.parse import urlparse

HTTP_URL_PATTERN = r'^http[s]*://.+'


def filter_urls(domain: str, urls: list[str]) -> list[str]:
    clean_urls = []
    for u in set(urls):
        if not u:
            continue
        clean_u = None
        if re.search(HTTP_URL_PATTERN, u):
            url_obj = urlparse(u)
            if domain in url_obj.netloc:
                clean_u = u
        else:
            if u.startswith("/"):
                u = u[1:]
            elif u.startswith("//"):
                u = u[2:]
            elif u.startswith("#") or u.startswith("mailto:") or u.startswith('java') or u.startswith('tel'):
                continue
            clean_u = "https://" + domain + "/" + u
        if clean_u:
            if clean_u.endswith("/"):
                clean_u = clean_u[:-1]
            clean_urls.append(clean_u)

    return clean_urls
