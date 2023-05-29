from datetime import datetime
from pydantic import BaseModel

class LinkInfo(BaseModel):
    id: int
    link: str
    title: str
    year: int
    rating: float
    votes: int
    created_at: datetime
    updated_at: datetime

class InputLinkInfo(BaseModel):
    link: str
    title: str
    year: int
    rating: float
    votes: int
