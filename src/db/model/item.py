from datetime import datetime
from pydantic import BaseModel

class Item(BaseModel):
    id: int
    file_id: int
    x: int
    y: int
    created_at: datetime
    updated_at: datetime

class InputItem(BaseModel):
    file_id: int
    x: int
    y: int
