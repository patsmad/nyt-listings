from datetime import datetime
from pydantic import BaseModel

class Box(BaseModel):
    id: int
    item_id: int
    left: int
    top: int
    width: int
    height: int
    created_at: datetime
    updated_at: datetime

class InputBox(BaseModel):
    item_id: int
    left: int
    top: int
    width: int
    height: int
