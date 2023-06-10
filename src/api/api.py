from .fetcher import Fetcher
from .updater import Updater
from src.model.annotated_file import AnnotatedFile
from src.model.file import File
from src.model.link_file import LinkFiles
from src.model.link import Link
from typing import Optional

class API:
    def __init__(self, fetcher: Fetcher, updater: Updater):
        self.fetcher = fetcher
        self.updater = updater

    def get_all_files(self) -> list[File]:
        return self.fetcher.get_all_files()

    def get_file_name(self, file_id: int) -> Optional[str]:
        return self.fetcher.get_file_name(file_id)

    def get_file(self, file_id: int) -> AnnotatedFile:
        return self.fetcher.get_file(file_id)

    def get_link(self, link: str) -> LinkFiles:
        return self.fetcher.get_link(link)

    def update_link(self, payload: dict) -> Optional[int]:
        link: Optional[Link] = self.fetcher.fetch_link(payload['id'])
        if link is not None:
            return self.updater.update_link(link, payload)

    def add_link(self, payload: dict) -> int:
        return self.updater.add_link(payload)
