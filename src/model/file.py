from __future__ import annotations
from pydantic import BaseModel
from src.db.model.file import File as DBFile

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
