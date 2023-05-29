from __future__ import annotations
from pydantic import BaseModel
from src.db.model.link import Link as DBLink
from .link_info import LinkInfo
from typing import Optional

class Link(BaseModel):
    id: int
    link: str
    confirmed: bool
    link_info: Optional[LinkInfo]

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'link': self.link,
            'confirmed': self.confirmed,
            'link_info': self.link_info.to_dict()
        }

    @staticmethod
    def from_db(link: DBLink, link_info: Optional[LinkInfo]) -> Link:
        return Link(**{
            'id': link.id,
            'link': link.link,
            'confirmed': link.confirmed,
            'link_info': link_info
        })

    @staticmethod
    def get_box_id_to_link_list(links: list[DBLink], links_info: dict[str, LinkInfo]) -> dict[int, list[Link]]:
        box_id_to_link_list: dict[int, list[Link]] = {}
        for link in links:
            if link.box_id not in box_id_to_link_list:
                box_id_to_link_list[link.box_id] = []
            box_id_to_link_list[link.box_id].append(Link.from_db(link, links_info.get(link.link)))
        return box_id_to_link_list
