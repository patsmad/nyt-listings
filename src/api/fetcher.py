from src.db.db import DB
from src.model.file import File
from src.model.item import Item

class Fetcher:
    def __init__(self, db: DB):
        self.db = db

    def get_all_files(self) -> list[File]:
        return [File.from_db(file) for file in self.db.fetch_all_files()]

    def get_all_items(self) -> list[Item]:
        file_dict = {file.id: file for file in self.get_all_files()}
        return [Item.from_db(item, file_dict[item.file_id]) for item in self.db.fetch_all_items()]
