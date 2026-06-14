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

def requestURLText(url, cache=True, cookie=None):
    with requestURL(url, cache) as request:
        return request.text
