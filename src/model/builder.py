from src.db.model.file import File as DBFile
from src.model.file import File

class FileBuilder:
    def fromDBFile(self, file: DBFile) -> File:
        return File(file.id, file.name)
