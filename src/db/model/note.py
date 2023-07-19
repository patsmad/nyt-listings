from datetime import datetime
from pydantic import BaseModel

class Note(BaseModel):
    id: int
    box_id: int
    note: str
    created_at: datetime
    updated_at: datetime

class InputNote(BaseModel):
    box_id: int
    note: str
