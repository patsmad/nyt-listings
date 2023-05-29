from datetime import datetime
from pydantic import BaseModel

class Link(BaseModel):
    id: int
    box_id: int
    link: str
    confirmed: bool
    created_at: datetime
    updated_at: datetime

class InputLink(BaseModel):
    box_id: int
    link: str
    confirmed: bool
