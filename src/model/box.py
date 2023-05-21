from __future__ import annotations
from pydantic import BaseModel
from src.db.model.box import Box as DBBox
from src.model.item import Item

class Box(BaseModel):
    id: int
    item: Item
    left: int
    top: int
    width: int
    height: int

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'item': self.item.to_dict(),
            'left': self.left,
            'top': self.top,
            'width': self.width,
            'height': self.height
        }

    @staticmethod
    def from_db(box: DBBox, item: Item) -> Box:
        return Box(**{
            'id': box.id,
            'item': item,
            'left': box.left,
            'top': box.top,
            'width': box.width,
            'height': box.height
        })