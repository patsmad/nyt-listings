from __future__ import annotations
from pydantic import BaseModel
from .box import Box
from .file import File
from .item import Item
from .link import Link
from .link_info import LinkInfo
from typing import Optional

class LinkFile(BaseModel):
    file_id: int
    file: str
    item_id: int
    x: int
    y: int
    box_id: int
    left: int
    top: int
    width: int
    height: int
    link_id: int
    confirmed: bool

    def to_dict(self) -> dict:
        return {
            'file_id': self.file_id,
            'file': self.file,
            'item_id': self.item_id,
            'x': self.x,
            'y': self.y,
            'box_id': self.box_id,
            'left': self.left,
            'top': self.top,
            'width': self.width,
            'height': self.height,
            'link_id': self.link_id,
            'confirmed': self.confirmed
        }

    @staticmethod
    def build(link: Link, link_id_to_file: dict[int, File], link_id_to_box: dict[int, Box], link_id_to_item: dict[int, Item]) -> LinkFile:
        file = link_id_to_file[link.id]
        box = link_id_to_box[link.id]
        item = link_id_to_item[link.id]
        return LinkFile(**{
            'file_id': file.id,
            'file': file.name,
            'item_id': item.id,
            'x': item.x,
            'y': item.y,
            'box_id': box.id,
            'left': box.left,
            'top': box.top,
            'width': box.width,
            'height': box.height,
            'link_id': link.id,
            'confirmed': link.confirmed
        })

class LinkFiles(BaseModel):
    link: str
    link_info: Optional[LinkInfo]
    link_files: list[LinkFile]

    def to_dict(self) -> dict:
        return {
            'link': self.link,
            'link_info': self.link_info.to_dict() if self.link_info is not None else None,
            'link_files': [link_file.to_dict() for link_file in self.link_files]
        }

    @staticmethod
    def build(link: str, link_info: Optional[LinkInfo], link_files: list[LinkFile]) -> LinkFiles:
        return LinkFiles(**{
            'link': link,
            'link_info': link_info,
            'link_files': link_files
        })
