from .fetcher import Fetcher
from src.model.file import File, AnnotatedFile

class API:
    def __init__(self, fetcher: Fetcher):
        self.fetcher = fetcher
    def get_all_files(self) -> list[File]:
        return self.fetcher.get_all_files()

    def get_file(self, file_id: int) -> AnnotatedFile:
        return self.fetcher.get_file(file_id)
