from __future__ import annotations
from pydantic import BaseModel
from src.db.model.item import Item as DBItem
from .box import Box

class Item(BaseModel):
    id: int
    x: int
    y: int
    boxes: list[Box]

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'boxes': [box.to_dict() for box in self.boxes]
        }

    @staticmethod
    def from_db(item: DBItem, boxes: list[Box]) -> Item:
        return Item(**{
            'id': item.id,
            'x': item.x,
            'y': item.y,
            'boxes': boxes
        })

    @staticmethod
    def get_list(items: list[DBItem], item_id_to_box: dict[int, list[Box]]) -> list[Item]:
        return [Item.from_db(item, item_id_to_box.get(item.id, [])) for item in items]
