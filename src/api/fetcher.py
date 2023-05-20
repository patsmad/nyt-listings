from src.db.db import DB
from src.model.builder import FileBuilder

class Fetcher:
    def __init__(self, db: DB, file_builder: FileBuilder):
        self.db = db
        self.file_builder = file_builder

    def get_all_files(self):
        return [self.file_builder.fromDBFile(file) for file in self.db.fetch_all_files()]
