from src.db.db import DB
from src.model.box import Box
from src.model.link import Link
from src.db.model.link import InputLink
from src.db.model.item import InputItem
from src.db.model.box import InputBox
from typing import Optional

class Updater:
    def __init__(self, db: DB):
        self.db = db

    def update_link(self, link: Link, payload: dict) -> Optional[int]:
        link.update(payload)
        return self.db.update_link(link)

    def add_link(self, payload: dict) -> int:
        link: InputLink = InputLink(**payload)
        return self.db.insert_link(link)

    def add_item(self, payload: dict) -> int:
        item: InputItem = InputItem(**payload)
        item_id = self.db.insert_item(item)
        box: InputBox = InputBox(**{
            'item_id': item_id,
            'left': item.x - 100,
            'top': item.y - 100,
            'width': 200,
            'height': 200,
            'channel': None,
            'time': None,
            'duration_minutes': None,
            'vcr_code': None
        })
        self.db.insert_box(box)
        return item_id

    def delete_item(self, payload: dict) -> Optional[int]:
        maybe_id = payload.get('id')
        if maybe_id is not None:
            return self.db.delete_item(maybe_id)

    def update_box(self, box: Box, payload: dict) -> Optional[int]:
        box.update(payload)
        return self.db.update_box(box)
