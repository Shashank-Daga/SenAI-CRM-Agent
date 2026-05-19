from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ThreadRead(BaseModel):
    id: str
    subject: Optional[str]
    priority: str
    created_at: datetime
    updated_at: datetime
    last_received_at: Optional[datetime]

    class Config:
        orm_mode = True
