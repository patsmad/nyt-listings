from __future__ import annotations
from pydantic import BaseModel
from src.db.model.file import File as DBFile
from .item import Item

class File(BaseModel):
    id: int
    name: str

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }

    @staticmethod
    def from_db(file: DBFile) -> File:
        return File(**{
            'id': file.id,
            'name': file.name
        })

class AnnotatedFile(BaseModel):
    id: int
    name: str
    items: list[Item]

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.to_dict() for item in self.items]
        }

    @staticmethod
    def from_db(file: DBFile, items: list[Item]) -> AnnotatedFile:
        return AnnotatedFile(**{
            'id': file.id,
            'name': file.name,
            'items': items
        })
