from .fetcher import Fetcher
from src.model.annotated_file import AnnotatedFile
from src.model.file import File
from src.model.link_file import LinkFiles

class API:
    def __init__(self, fetcher: Fetcher):
        self.fetcher = fetcher
    def get_all_files(self) -> list[File]:
        return self.fetcher.get_all_files()

    def get_file(self, file_id: int) -> AnnotatedFile:
        return self.fetcher.get_file(file_id)

    def get_link(self, link: str) -> LinkFiles:
        return self.fetcher.get_link(link)
