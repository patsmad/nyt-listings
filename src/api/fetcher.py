from src.db.db import DB
from src.db.model.link import Link as DBLink
from src.db.model.box import Box as DBBox
from src.db.model.note import Note as DBNote
from src.model.annotated_file import AnnotatedFile
from src.model.file import File
from src.model.item import Item
from src.model.box import Box
from src.model.link import Link
from src.model.note import Note
from src.model.link_file import LinkFile, LinkFiles
from src.model.link_info import LinkInfo
from typing import Optional

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
        link_id_to_notes: dict[int, list[Note]] = {link_id: [Note.from_db(note) for note in notes] for link_id, notes in self.db.fetch_link_id_to_notes(link).items()}
        link_files: list[LinkFile] = [LinkFile.build(link, link_id_to_files, link_id_to_boxes, link_id_to_items, link_id_to_notes) for link in links]
        return LinkFiles.build(link, link_info, link_files)

    def fetch_link(self, link_id: int) -> Optional[Link]:
        db_link: Optional[DBLink] = self.db.fetch_link(link_id)
        if db_link is not None:
            link_info: Optional[LinkInfo] = LinkInfo.from_db(self.db.get_link_info(db_link.link))
            return Link.from_db(db_link, link_info=link_info)

    def fetch_box(self, box_id: int) -> Optional[Box]:
        db_box: Optional[DBBox] = self.db.fetch_box(box_id)
        if db_box is not None:
            links = [Link.from_db(link, self.db.get_link_info(link.link)) for link in self.db.fetch_box_links(db_box.id)]
            return Box.from_db(db_box, links)

    def fetch_note(self, note_id: int) -> Optional[Note]:
        db_note: Optional[DBNote] = self.db.fetch_note(note_id)
        if db_note is not None:
            return Note.from_db(db_note)
