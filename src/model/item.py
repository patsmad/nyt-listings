from __future__ import annotations
from pydantic import BaseModel
from src.db.model.item import Item as DBItem
from src.model.file import File

class Item(BaseModel):
    id: int
    file: File
    x: int
    y: int

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'file': self.file.to_dict(),
            'x': self.x,
            'y': self.y
        }

    @staticmethod
    def from_db(item: DBItem, file: File) -> Item:
        return Item(**{
            'id': item.id,
            'file': file,
            'x': item.x,
            'y': item.y
        })
