from __future__ import annotations
from pydantic import BaseModel
from src.db.model.box import Box as DBBox
from .link import Link

class Box(BaseModel):
    id: int
    left: int
    top: int
    width: int
    height: int
    links: list[Link]

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'left': self.left,
            'top': self.top,
            'width': self.width,
            'height': self.height,
            'links': [link.to_dict() for link in self.links]
        }

    @staticmethod
    def from_db(box: DBBox, links: list[Link]) -> Box:
        return Box(**{
            'id': box.id,
            'left': box.left,
            'top': box.top,
            'width': box.width,
            'height': box.height,
            'links': links
        })

    def update(self, payload: dict) -> None:
        if 'left' in payload:
            self.left = payload['left']
        if 'top' in payload:
            self.top = payload['top']
        if 'width' in payload:
            self.width = payload['width']
        if 'height' in payload:
            self.height = payload['height']

    @staticmethod
    def get_item_id_to_box_list(boxes: list[DBBox], box_id_to_links: dict[int, list[Link]]) -> dict[int, list[Box]]:
        item_id_to_box_list: dict[int, list[Box]] = {}
        for box in boxes:
            if box.item_id not in item_id_to_box_list:
                item_id_to_box_list[box.item_id] = []
            item_id_to_box_list[box.item_id].append(Box.from_db(box, box_id_to_links.get(box.id, [])))
        return item_id_to_box_list
