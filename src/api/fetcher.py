from src.db.db import DB
from src.db.model.link import Link as DBLink
from src.db.model.link_info import LinkInfo as DBLinkInfo
from src.db.model.box import Box as DBBox
from src.model.annotated_file import AnnotatedFile
from src.model.file import File
from src.model.item import Item
from src.model.box import Box
from src.model.link import Link
from src.model.link_file import LinkFile, LinkFiles
from src.model.link_info import LinkInfo
from typing import List, Optional
from fuzzywuzzy import fuzz

class Fetcher:
    def __init__(self, db: DB):
        self.db = db

    def get_all_files(self) -> list[File]:
        return [File.from_db(file) for file in self.db.fetch_all_files()]

    def get_file_name(self, file_id: int) -> Optional[str]:
        file_db = self.db.fetch_file(file_id)
        if file_db is not None:
            return file_db.name

    def get_file(self, file_id: id) -> AnnotatedFile:
        link_to_link_info: dict[str, LinkInfo] = LinkInfo.get_link_to_link_info(self.db.fetch_file_links_info(file_id))
        box_id_to_link: dict[int, list[Link]] = Link.get_box_id_to_link_list(self.db.fetch_file_links(file_id), link_to_link_info)
        item_id_to_box: dict[int, list[Box]] = Box.get_item_id_to_box_list(self.db.fetch_file_boxes(file_id), box_id_to_link)
        item_list: list[Item] = Item.get_list(self.db.fetch_file_items(file_id), item_id_to_box)
        return AnnotatedFile.from_db(self.db.fetch_file(file_id), item_list)

    def get_link(self, link: str) -> LinkFiles:
        link_info: Optional[LinkInfo] = LinkInfo.from_db(self.db.get_link_info(link))
        links: list[Link] = [Link.from_db(l, link_info) for l in self.db.fetch_all_links_for_link(link)]
        link_map: dict[int, Link] = {l.id: l for l in links}
        link_id_to_boxes: dict[int, Box] = {link_id: Box.from_db(box, [link_map[link_id]]) for link_id, box in self.db.fetch_link_id_to_boxes(link).items()}
        link_id_to_items: dict[int, Item] = {link_id: Item.from_db(item, [link_id_to_boxes[link_id]]) for link_id, item in self.db.fetch_link_id_to_items(link).items()}
        link_id_to_files: dict[int, File] = {link_id: File.from_db(file) for link_id, file in self.db.fetch_link_id_to_files(link).items()}
        link_files: list[LinkFile] = [LinkFile.build(link, link_id_to_files, link_id_to_boxes, link_id_to_items) for link in links]
        return LinkFiles.build(link, link_info, link_files)

    def search_title(self, title: str) -> List[LinkInfo]:
        link_infos = sorted(
            self.db.fetch_all_link_info(),
            key=lambda link_info: fuzz.ratio(link_info.title, title),
            reverse=True
        )[:20]
        return [LinkInfo.from_db(link_info) for link_info in link_infos]

    def search_year(self, year: int) -> List[LinkInfo]:
        link_infos = sorted(
            self.db.fetch_year_link_info(year),
            key=lambda link_info: link_info.votes,
            reverse=True
        )
        return [LinkInfo.from_db(link_info) for link_info in link_infos]

    def count(self, link: str) -> int:
        return self.db.count(link)

    def fetch_link(self, link_id: int) -> Optional[Link]:
        db_link: Optional[DBLink] = self.db.fetch_link(link_id)
        if db_link is not None:
            link_info: Optional[LinkInfo] = LinkInfo.from_db(self.db.get_link_info(db_link.link))
            return Link.from_db(db_link, link_info=link_info)

    def fetch_link_info_by_title(self, title: str) -> Optional[LinkInfo]:
        db_link_info: Optional[DBLinkInfo] = self.db.fetch_link_info_by_title(title)
        if db_link_info is not None:
            return LinkInfo.from_db(db_link_info)

    def fetch_box(self, box_id: int) -> Optional[Box]:
        db_box: Optional[DBBox] = self.db.fetch_box(box_id)
        if db_box is not None:
            links = [Link.from_db(link, LinkInfo.from_db(self.db.get_link_info(link.link))) for link in self.db.fetch_box_links(db_box.id)]
            return Box.from_db(db_box, links)
