from __future__ import annotations
from pydantic import BaseModel
from src.db.model.note import Note as DBNote

class Note(BaseModel):
    id: int
    note: str

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'note': self.note,
        }

    @staticmethod
    def from_db(note: DBNote) -> Note:
        return Note(**{
            'id': note.id,
            'note': note.note
        })

    def update(self, payload: dict) -> None:
        if 'note' in payload:
            self.note = payload['note']

    @staticmethod
    def get_box_id_to_note_list(notes: list[DBNote]) -> dict[int, list[Note]]:
        box_id_to_note_list: dict[int, list[Note]] = {}
        for note in notes:
            if note.box_id not in box_id_to_note_list:
                box_id_to_note_list[note.box_id] = []
            box_id_to_note_list[note.box_id].append(Note.from_db(note))
        return box_id_to_note_list
