from .fetcher import Fetcher
from src.model.file import File
from src.model.item import Item

class API:
    def __init__(self, fetcher: Fetcher):
        self.fetcher = fetcher
    def get_all_files(self) -> list[File]:
        return self.fetcher.get_all_files()

    def get_all_items(self) -> list[Item]:
        return self.fetcher.get_all_items()
