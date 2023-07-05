from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Box(BaseModel):
    id: int
    item_id: int
    left: int
    top: int
    width: int
    height: int
    channel: Optional[str]
    time: Optional[datetime]
    duration_minutes: Optional[int]
    vcr_code: Optional[int]
    created_at: datetime
    updated_at: datetime

class InputBox(BaseModel):
    item_id: int
    left: int
    top: int
    width: int
    height: int
    channel: Optional[str]
    time: Optional[datetime]
    duration_minutes: Optional[int]
    vcr_code: Optional[int]
