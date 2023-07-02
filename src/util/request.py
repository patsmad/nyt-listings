from bs4 import BeautifulSoup as BS
from requests import get, Response
from src.util.config import Config

headers: dict = Config().headers
max_retries: int = 5

def retryGet(url: str, retry: int, cache: bool = True) -> Response:
    if retry < max_retries:
        try:
            out: Response = get(url, timeout=60.0, headers=headers)
            return out
        except:
            print(f"Retry {url}")
            return retryGet(url, retry + 1, cache)
    else:
        raise Exception("ABORT")

def requestURL(url: str, cache: bool = True) -> Response:
    return retryGet(url, 0, cache)

def soupifyURL(url: str, cache: bool = True) -> BS:
    with requestURL(url, cache) as request:
        return BS(request.text, 'html.parser')
