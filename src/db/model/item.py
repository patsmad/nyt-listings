from datetime import datetime
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    filename: str
    x: int
    y: int
    created_at: datetime
    updated_at: datetime