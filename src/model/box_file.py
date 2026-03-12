from __future__ import annotations
from pydantic import BaseModel
from .box import Box
from .file import File
from .item import Item
from typing import Optional
from datetime import datetime

class BoxFile(BaseModel):
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
            'vcr_code': self.vcr_code
        }

    @staticmethod
    def build(box: Box, box_id_to_file: dict[int, File], box_id_to_item: dict[int, Item]) -> BoxFile:
        file = box_id_to_file[box.id]
        item = box_id_to_item[box.id]
        return BoxFile(**{
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
            'vcr_code': box.vcr_code
        })
