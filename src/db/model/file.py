from datetime import datetime
from pydantic import BaseModel

class File(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

class InputFile(BaseModel):
    name: str
