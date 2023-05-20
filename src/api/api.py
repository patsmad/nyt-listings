from .fetcher import Fetcher

class API:
    def __init__(self, fetcher: Fetcher):
        self.fetcher = fetcher
    def get_all_files(self) -> list:
        return self.fetcher.get_all_files()
