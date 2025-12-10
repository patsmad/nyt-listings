from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class File(BaseModel):
    id: int
    name: str
    file_date: Optional[datetime]
    width: Optional[int]
    height: Optional[int]
    created_at: datetime
    updated_at: datetime

class InputFile(BaseModel):
    name: str
    file_date: Optional[datetime]
    width: Optional[int]
    height: Optional[int]
