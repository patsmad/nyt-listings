from src.db.db import DB
from src.model.file import File
from src.model.item import Item
from src.model.box import Box
from src.model.link import Link

class Fetcher:
    def __init__(self, db: DB):
        self.db = db

    def get_all_files(self) -> list[File]:
        return [File.from_db(file) for file in self.db.fetch_all_files()]

    def get_all_items(self) -> list[Item]:
        file_dict: dict[int, File] = {file.id: file for file in self.get_all_files()}
        return [
            Item.from_db(item, file_dict[item.file_id])
            for item in self.db.fetch_all_items()
            if item.file_id in file_dict
        ]

    def get_all_boxes(self) -> list[Box]:
        item_dict: dict[int, Item] = {item.id: item for item in self.get_all_items()}
        return [
            Box.from_db(box, item_dict[box.item_id])
            for box in self.db.fetch_all_boxes()
            if box.item_id in item_dict
        ]

    def get_all_links(self) -> list[Link]:
        box_dict: dict[int, Box] = {box.id: box for box in self.get_all_boxes()}
        return [
            Link.from_db(link, box_dict[link.box_id])
            for link in self.db.fetch_all_links()
            if link.box_id in box_dict
        ]
