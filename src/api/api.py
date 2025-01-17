from .fetcher import Fetcher
from .updater import Updater
from src.model.annotated_file import AnnotatedFile
from src.model.file import File
from src.model.link_file import LinkFiles
from src.model.link import Link
from src.model.link_info import LinkInfo
from src.model.box import Box
from typing import List, Optional

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

    def search_title(self, title: str) -> List[LinkInfo]:
        return self.fetcher.search_title(title)

    def get_count(self, link: str) -> int:
        return self.fetcher.count(link)

    def get_box(self, box_id: int) -> Optional[Box]:
        return self.fetcher.fetch_box(box_id)

    def update_link(self, payload: dict) -> Optional[int]:
        link: Optional[Link] = self.fetcher.fetch_link(payload['id'])
        if link is not None:
            return self.updater.update_link(link, payload)

    def update_title(self, payload: dict) -> Optional[int]:
        link: Optional[Link] = self.fetcher.fetch_link(payload['id'])
        if link is not None:
            link_info: Optional[LinkInfo] = self.fetcher.fetch_link_info_by_title(payload['title'])
            if link_info is not None:
                payload['link'] = link_info.link
                return self.updater.update_link(link, payload)
            else:
                return link.id

    def add_link(self, payload: dict) -> int:
        return self.updater.add_link(payload)

    def add_title(self, payload: dict) -> int:
        link_info: Optional[LinkInfo] = self.fetcher.fetch_link_info_by_title(payload['title'])
        if link_info is not None:
            payload['link'] = link_info.link
            return self.updater.add_link(payload)

    def add_item(self, payload: dict) -> int:
        return self.updater.add_item(payload)

    def delete_item(self, payload: dict) -> Optional[int]:
        return self.updater.delete_item(payload)

    def update_box(self, payload: dict) -> Optional[int]:
        box: Optional[Box] = self.fetcher.fetch_box(payload['id'])
        if box is not None:
            return self.updater.update_box(box, payload)
