from __future__ import annotations
from pydantic import BaseModel
from src.db.model.link_info import LinkInfo as DBLinkInfo
from typing import Optional

class LinkInfo(BaseModel):
    id: int
    link: str
    title: str
    rating: float
    votes: int
    year: int

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'link': self.link,
            'title': self.title,
            'rating': self.rating,
            'votes': self.votes,
            'year': self.year
        }

    @staticmethod
    def from_db(link_info: Optional[DBLinkInfo]) -> Optional[LinkInfo]:
        if link_info is not None:
            return LinkInfo(**{
                'id': link_info.id,
                'link': link_info.link,
                'title': link_info.title,
                'rating': link_info.rating,
                'votes': link_info.votes,
                'year': link_info.year
            })

    @staticmethod
    def get_link_to_link_info(links_info: list[DBLinkInfo]) -> dict[str, LinkInfo]:
        return {link_info.link: LinkInfo.from_db(link_info) for link_info in links_info}
