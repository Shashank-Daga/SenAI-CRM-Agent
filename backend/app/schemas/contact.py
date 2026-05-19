from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class ContactRead(BaseModel):
    id: str
    email: EmailStr
    name: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
