from src.db.db import DB
from src.model.box import Box
from src.model.link import Link
from src.db.model.link import InputLink
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

    def delete_item(self, payload: dict) -> Optional[int]:
        maybe_id = payload.get('id')
        if maybe_id is not None:
            return self.db.delete_item(maybe_id)

    def update_box(self, box: Box, payload: dict) -> Optional[int]:
        print(box)
        print(payload)
        box.update(payload)
        print(box)
        return None
        #return self.db.update_box(box)
