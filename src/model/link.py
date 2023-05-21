from __future__ import annotations
from pydantic import BaseModel
from src.db.model.link import Link as DBLink
from src.model.box import Box

class Link(BaseModel):
    id: int
    box: Box
    link: str
    confirmed: bool

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'box': self.box.to_dict(),
            'link': self.link,
            'confirmed': self.confirmed
        }

    @staticmethod
    def from_db(link: DBLink, box: Box) -> Link:
        return Link(**{
            'id': link.id,
            'box': box,
            'link': link.link,
            'confirmed': link.confirmed
        })