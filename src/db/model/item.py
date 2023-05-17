from pydantic import BaseModel
from datetime import datetime

class Item(BaseModel):
    id: int
    filename: str
    x: int
    y: int
    created_at: datetime
    updated_at: datetime
