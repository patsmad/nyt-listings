
class File:
    def __init__(self, id: int | None, name: str):
        self.id = id
        self.name = name

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }
