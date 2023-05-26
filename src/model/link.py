from __future__ import annotations
from pydantic import BaseModel
from src.db.model.link import Link as DBLink

class Link(BaseModel):
    id: int
    link: str
    confirmed: bool

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'link': self.link,
            'confirmed': self.confirmed
        }

    @staticmethod
    def from_db(link: DBLink) -> Link:
        return Link(**{
            'id': link.id,
            'link': link.link,
            'confirmed': link.confirmed
        })

    @staticmethod
    def get_box_id_to_link_list(links: list[DBLink]) -> dict[int, list[Link]]:
        box_id_to_link_list: dict[int, list[Link]] = {}
        for link in links:
            if link.box_id not in box_id_to_link_list:
                box_id_to_link_list[link.box_id] = []
            box_id_to_link_list[link.box_id].append(Link.from_db(link))
        return box_id_to_link_list
