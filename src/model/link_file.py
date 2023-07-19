from __future__ import annotations
from pydantic import BaseModel
from .box import Box
from .file import File
from .item import Item
from .link import Link
from .link_info import LinkInfo
from typing import Optional
from datetime import datetime

class LinkFile(BaseModel):
    file_id: int
    file: str
    file_date: datetime
    item_id: int
    x: int
    y: int
    box_id: int
    left: int
    top: int
    width: int
    height: int
    channel: Optional[str]
    time: Optional[datetime]
    duration_minutes: Optional[int]
    vcr_code: Optional[int]
    link_id: int
    confirmed: bool
    notes: list[str]

    def to_dict(self) -> dict:
        return {
            'file_id': self.file_id,
            'file': self.file,
            'file_date': self.file_date,
            'item_id': self.item_id,
            'x': self.x,
            'y': self.y,
            'box_id': self.box_id,
            'left': self.left,
            'top': self.top,
            'width': self.width,
            'height': self.height,
            'channel': self.channel,
            'time': self.time,
            'duration_minutes': self.duration_minutes,
            'vcr_code': self.vcr_code,
            'link_id': self.link_id,
            'confirmed': self.confirmed,
            'notes': self.notes
        }

    @staticmethod
    def build(
        link: Link,
        link_id_to_file: dict[int, File],
        link_id_to_box: dict[int, Box],
        link_id_to_item: dict[int, Item],
        link_id_to_notes: dict[int, list[Note]]
    ) -> LinkFile:
        file = link_id_to_file[link.id]
        box = link_id_to_box[link.id]
        item = link_id_to_item[link.id]
        notes = link_id_to_notes[link.id]
        return LinkFile(**{
            'file_id': file.id,
            'file': file.name,
            'file_date': file.file_date,
            'item_id': item.id,
            'x': item.x,
            'y': item.y,
            'box_id': box.id,
            'left': box.left,
            'top': box.top,
            'width': box.width,
            'height': box.height,
            'channel': box.channel,
            'time': box.time,
            'duration_minutes': box.duration_minutes,
            'vcr_code': box.vcr_code,
            'link_id': link.id,
            'confirmed': link.confirmed,
            'notes': notes
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
