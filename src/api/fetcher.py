from src.db.db import DB
from src.model.annotated_file import AnnotatedFile
from src.model.file import File
from src.model.item import Item
from src.model.box import Box
from src.model.link import Link
from src.model.link_file import LinkFile, LinkFiles
from src.model.link_info import LinkInfo
from typing import Optional

class Fetcher:
    def __init__(self, db: DB):
        self.db = db

    def get_all_files(self) -> list[File]:
        return [File.from_db(file) for file in self.db.fetch_all_files()]

    def get_file(self, file_id: id) -> AnnotatedFile:
        link_to_link_info: dict[str, LinkInfo] = LinkInfo.get_link_to_link_info(self.db.fetch_file_links_info(file_id))
        box_id_to_link: dict[int, list[Link]] = Link.get_box_id_to_link_list(self.db.fetch_file_links(file_id), link_to_link_info)
        item_id_to_box: dict[int, list[Box]] = Box.get_item_id_to_box_list(self.db.fetch_file_boxes(file_id), box_id_to_link)
        item_list: list[Item] = Item.get_list(self.db.fetch_file_items(file_id), item_id_to_box)
        return AnnotatedFile.from_db(self.db.fetch_file(file_id), item_list)

    def get_link(self, link: str) -> LinkFiles:
        link_info: Optional[LinkInfo] = LinkInfo.from_db(self.db.get_link_info(link))
        links: list[Link] = [Link.from_db(l, link_info) for l in self.db.fetch_all_links_for_link(link)]
        link_id_to_files: dict[int, File] = {link_id: File.from_db(file) for link_id, file in self.db.fetch_link_id_to_files(link).items()}
        link_files: list[LinkFile] = [LinkFile.build(l, link_id_to_files) for l in links]
        return LinkFiles.build(link, link_info, link_files)
