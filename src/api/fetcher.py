import itertools
from src.db.db import DB
from src.model.file import File, AnnotatedFile
from src.model.item import Item
from src.model.box import Box
from src.model.link import Link
from src.model.link_info import LinkInfo

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
