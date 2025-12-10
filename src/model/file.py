from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel
from src.db.model.file import File as DBFile
from typing import Optional

class File(BaseModel):
    id: int
    name: str
    file_date: Optional[datetime]
    width: Optional[int]
    height: Optional[int]

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'file_date': self.file_date,
            'width': self.width,
            'height': self.height
        }

    @staticmethod
    def from_db(file: DBFile) -> File:
        return File(**{
            'id': file.id,
            'name': file.name,
            'file_date': file.file_date,
            'width': file.width,
            'height': file.height
        })
