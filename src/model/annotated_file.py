from __future__ import annotations
from pydantic import BaseModel
from src.db.model.file import File as DBFile
from .item import Item
from datetime import datetime

class AnnotatedFile(BaseModel):
    id: int
    name: str
    file_date: datetime
    items: list[Item]

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'file_date': self.file_date,
            'items': [item.to_dict() for item in self.items]
        }

    @staticmethod
    def from_db(file: DBFile, items: list[Item]) -> AnnotatedFile:
        return AnnotatedFile(**{
            'id': file.id,
            'name': file.name,
            'file_date': file.file_date,
            'items': items
        })
