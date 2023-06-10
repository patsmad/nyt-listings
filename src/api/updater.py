from src.db.db import DB
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
