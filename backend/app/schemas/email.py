from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class EmailIngestPayload(BaseModel):
    message_id: str = Field(..., min_length=1, max_length=512)
    sender: EmailStr
    recipient: EmailStr
    subject: Optional[str] = Field(None, max_length=512)
    body: Optional[str] = Field(None)
    received_at: datetime
    thread_id: Optional[str] = Field(None, max_length=64)
    thread_subject: Optional[str] = Field(None, max_length=512)

    @field_validator("subject", "body", mode="before")
    @classmethod
    def normalize_text(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        stripped = value.strip()
        return stripped if stripped else None

    @model_validator(mode="after")
    def require_subject_or_body(self) -> "EmailIngestPayload":
        if not self.subject and not self.body:
            raise ValueError("Email must include either a subject or a body.")
        return self


class EmailIngestResult(BaseModel):
    job_id: str
    status: str
    thread_id: str
    message_id: str
    priority: str
    is_duplicate: bool
    details: Optional[Any] = None


class StandardResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    error_code: Optional[str] = None
    details: Optional[Any] = None


class ErrorResponse(BaseModel):
    success: bool = False
    error_code: str
    message: str
    details: Optional[Any] = None
